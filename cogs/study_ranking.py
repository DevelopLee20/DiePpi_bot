import logging
from datetime import datetime

import discord
from discord.ext import commands

from cogs.base_cog import BaseCog
from core.messages import yesterday_ranking_message
from db.attend_collection import AttendCollection
from db.study_collection import StudyCollection
from utils.time_utils import get_study_day_range

logger = logging.getLogger(__name__)


class StudyRanking(BaseCog):
    """공부 순위를 표시하는 Cog."""

    def __init__(self, bot: commands.Bot) -> None:
        """StudyRanking 초기화.

        Args:
            bot: Discord bot 인스턴스
        """
        super().__init__(bot)
        self.last_ranking_date: datetime | None = None

    def _is_study_channel_join(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> bool:
        """공부방 입장 여부를 확인합니다."""
        config = self.bot.config
        return (
            after.channel
            and after.channel.name == config.study_channel
            and before.channel != after.channel
        )

    async def _should_show_ranking(self) -> bool:
        """오늘 첫 번째 입장자인지 확인합니다."""
        now = datetime.now()
        today_start, today_end = get_study_day_range(now)

        # 이미 오늘(오전 6시 기준) 순위를 표시했는지 먼저 확인 (Race Condition 방지)
        if self.last_ranking_date:
            last_start, last_end = get_study_day_range(self.last_ranking_date)
            if last_start == today_start:
                return False

        # 오늘 출석한 유저가 있는지 확인 (오전 6시 이후 기준)
        attended_users = await AttendCollection.get_today_attended_user_ids()
        if len(attended_users) > 0:
            return False

        # 순위 표시 직전에 날짜를 먼저 업데이트 (중복 방지)
        self.last_ranking_date = datetime.now()
        return True

    async def _show_yesterday_ranking(self, alert_channel: discord.TextChannel) -> None:
        """어제의 공부 순위 top3를 표시합니다."""
        try:
            rankings_data = await StudyCollection.get_yesterday_top_rankings(limit=3)

            if not rankings_data:
                await alert_channel.send("📊 어제 공부 기록이 없다 삐!")
                return

            # user_id를 mention으로 변환
            guild = alert_channel.guild
            rankings = []
            for rank in rankings_data:
                user_id = rank["user_id"]
                total_min = rank["total_min"]
                member = guild.get_member(int(user_id))
                user_mention = member.mention if member else f"<@{user_id}>"
                rankings.append((user_mention, total_min))

            message = yesterday_ranking_message(rankings)
            await alert_channel.send(message)
        except Exception as e:
            logger.error(f"어제 순위 표시 중 오류 발생: {e}", exc_info=True)
            raise

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        """음성 채널 상태가 변경될 때 자동으로 호출되는 이벤트."""
        # 봇은 무시
        if member.bot:
            return

        guild = member.guild
        alert_channel = self.get_alert_channel(guild)

        if not alert_channel:
            return

        # 공부방 입장 확인
        if self._is_study_channel_join(member, before, after):
            # 오늘 첫 번째 입장자인지 확인
            if await self._should_show_ranking():
                try:
                    await self._show_yesterday_ranking(alert_channel)
                except Exception as e:
                    # 오류 발생 시 로그만 남기고 계속 진행
                    logger.error(f"순위 표시 실패했지만 계속 진행: {e}")


async def setup(bot):
    await bot.add_cog(StudyRanking(bot))
