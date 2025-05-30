from datetime import datetime

import discord
from discord.ext import commands

from core.enums import Mode
from core.env import env
from core.messages import end_study_message, start_study_message
from db.study_collection import StudyCollection
from models.study_model import StudyModel


class StudyTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # 봇 인스턴스
        self.user_voice_times = (
            {}
        )  # 각 유저의 입장 시간을 저장하는 딕셔너리 (key: user.id, value: 입장 시간)
        if env.MODE == Mode.PROD.value:
            print("☑️ PROD mode.")
            self.study_channel_name = "공부방"
            self.alert_channel_name = "스터디-알림"
        else:
            print("☑️ DEV mode.")
            self.study_channel_name = "디스코드-봇-만드는-채널"
            self.alert_channel_name = "디스코드-봇-만드는-채널"

    @commands.Cog.listener()  # 음성 채널 상태가 변경될 때 자동으로 호출
    async def on_voice_state_update(self, member, before, after):
        """
        음성 채널 상태가 변경될 때 자동으로 호출되는 이벤트
        예: 음성 채널 입장, 퇴장, 이동 시 작동
        """
        guild = member.guild  # 유저가 속한 서버 객체

        # 모든 채널 조회 후 이름과 맞는 채널만 반환
        alert_channel = discord.utils.get(
            guild.text_channels, name=self.alert_channel_name
        )

        # ✅ 사용자가 '공부방'에 새로 입장했을 때
        if (
            member.id not in self.user_voice_times
            and after.channel
            and after.channel.name == self.study_channel_name
        ):
            self.user_voice_times[member.id] = datetime.now()

            if alert_channel:
                await alert_channel.send(start_study_message(member.mention))

        # ✅ 사용자가 '공부방'에서 나가거나 다른 채널로 이동한 경우
        elif (
            before.channel
            and before.channel.name == self.study_channel_name
            and (after.channel != before.channel)
        ):
            # 저장된 입장 시간 가져오기 (없으면 None)
            start_time = self.user_voice_times.pop(member.id, None)
            if start_time:
                end_time = datetime.now()  # 퇴장 시간
                duration = (
                    end_time - start_time
                )  # 공부한 전체 시간 (datetime.timedelta)
                minutes = int(duration.total_seconds() // 60)  # 분 단위로 환산

                # 텍스트 알림 채널 찾기
                if alert_channel:
                    # DB에 공부 기록 저장
                    study_record = StudyModel(
                        user_id=str(member.id),
                        start_time=start_time,
                        end_time=end_time,
                        total_min=minutes,
                    )

                    await StudyCollection.insert_study(study_record)
                    total_minutes = await StudyCollection.find_total_study_min_in_today(
                        str(member.id)
                    )

                    # 총 공부량 메시지 보내기
                    await alert_channel.send(
                        end_study_message(member.mention, minutes, total_minutes)
                    )


# Cog 등록을 위한 필수 비동기 setup 함수
async def setup(bot):
    await bot.add_cog(StudyTracker(bot))
