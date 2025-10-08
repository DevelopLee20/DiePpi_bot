import logging
from datetime import datetime

import discord
from discord.ext import commands

from cogs.base_cog import BaseCog
from core.env import env
from core.messages import attend_study_message, end_study_message, start_study_message
from db.attend_collection import AttendCollection
from db.study_collection import StudyCollection
from models.study_model import StudyModel

logger = logging.getLogger(__name__)


class StudyTracker(BaseCog):
    """음성 채널 입장/퇴장을 추적하여 공부 시간을 기록하는 Cog."""

    def __init__(self, bot: commands.Bot) -> None:
        """StudyTracker 초기화.

        Args:
            bot: Discord bot 인스턴스
        """
        super().__init__(bot)
        self.user_voice_times: dict[int, datetime] = {}

    def _is_study_channel_join(
        self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ) -> bool:
        """공부방 입장 여부를 확인합니다."""
        config = self.bot.config
        return (
            member.id not in self.user_voice_times
            and after.channel
            and after.channel.name == config.study_channel
        )

    def _is_study_channel_leave(self, before: discord.VoiceState, after: discord.VoiceState) -> bool:
        """공부방 퇴장 여부를 확인합니다."""
        config = self.bot.config
        return (
            before.channel
            and before.channel.name == config.study_channel
            and after.channel != before.channel
        )

    async def _handle_study_start(self, member: discord.Member, alert_channel: discord.TextChannel | None) -> None:
        """공부 시작을 처리합니다."""
        self.user_voice_times[member.id] = datetime.now()

        if alert_channel:
            await alert_channel.send(start_study_message(member.mention))

            # 최초 1회만 출석체크
            try:
                if not await AttendCollection.get_today_user_is_attend(str(member.id)):
                    await AttendCollection.insert_attend(str(member.id), datetime.now())
                    await alert_channel.send(attend_study_message(member.mention))
            except Exception as e:
                logger.error(f"출석 체크 중 오류 발생: {e}")

    async def _handle_study_end(self, member: discord.Member, alert_channel: discord.TextChannel | None) -> None:
        """공부 종료를 처리합니다."""
        start_time = self.user_voice_times.pop(member.id, None)
        if not start_time:
            return

        end_time = datetime.now()
        duration = end_time - start_time
        minutes = int(duration.total_seconds() // 60)

        if not alert_channel:
            return

        study_record = StudyModel(
            user_id=str(member.id),
            start_time=start_time,
            end_time=end_time,
            total_min=minutes,
        )

        try:
            await StudyCollection.insert_study(study_record)
            total_minutes = await StudyCollection.find_total_study_min_in_today(str(member.id))

            gemini_client = self.bot.get_gemini_client(
                env.GEMINI_STUDY_ENCOURAGEMENT_INSTRUCTION)
            status, text = await gemini_client.create_gemini_message(f"공부시간:{total_minutes}분")

            await alert_channel.send(
                end_study_message(member.mention, minutes,
                                  total_minutes, text, status)
            )
        except Exception as e:
            logger.error(f"공부 기록 저장 중 오류 발생: {e}")
            if alert_channel:
                await alert_channel.send(f"{member.mention}님의 공부 기록 저장 중 오류가 발생했다 삐!")

    @commands.Cog.listener()  # 음성 채널 상태가 변경될 때 자동으로 호출
    async def on_voice_state_update(
        self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ) -> None:
        """
        음성 채널 상태가 변경될 때 자동으로 호출되는 이벤트
        예: 음성 채널 입장, 퇴장, 이동 시 작동
        """
        guild = member.guild
        alert_channel = self.get_alert_channel(guild)

        if self._is_study_channel_join(member, before, after):
            await self._handle_study_start(member, alert_channel)
        elif self._is_study_channel_leave(before, after):
            await self._handle_study_end(member, alert_channel)


# Cog 등록을 위한 필수 비동기 setup 함수
async def setup(bot):
    await bot.add_cog(StudyTracker(bot))
