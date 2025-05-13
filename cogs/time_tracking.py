from discord.ext import commands
import discord
from datetime import datetime
from zoneinfo import ZoneInfo

from core.enums import GoodJobMessage

class StudyTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot                                 # 봇 인스턴스
        self.user_voice_times = {}                     # 각 유저의 입장 시간을 저장하는 딕셔너리 (key: user.id, value: 입장 시간)
        self.study_channel_name = "공부방"               # 추적할 음성 채널 이름
        self.alert_channel_name = "디스코드-봇-만드는-채널"  # 로그를 보낼 테스트용 텍스트 채널 이름
        # self.alert_channel_name = "스터디-알림"           # 로그를 보낼 텍스트 채널 이름
        self.kst = ZoneInfo("Asia/Seoul")               # ✅ 한국 시간대 설정

    @commands.Cog.listener() # 음성 채널 상태가 변경될 때 자동으로 호출
    async def on_voice_state_update(self, member, before, after):
        """
        음성 채널 상태가 변경될 때 자동으로 호출되는 이벤트
        예: 음성 채널 입장, 퇴장, 이동 시 작동
        """
        guild = member.guild  # 유저가 속한 서버 객체
        
        # 모든 채널 조회 후 이름과 맞는 채널만 반환
        alert_channel = discord.utils.get(guild.text_channels, name=self.alert_channel_name)

        # ✅ 사용자가 '공부방'에 새로 입장했을 때
        if after.channel and after.channel.name == self.study_channel_name:
            self.user_voice_times[member.id] = datetime.now(self.kst)

            # 알림 보낼 텍스트 채널 찾기
            alert_channel = discord.utils.get(guild.text_channels, name=self.alert_channel_name)
            if alert_channel:
                now = datetime.now(self.kst).strftime('%Y-%m-%d %H:%M:%S')  # 현재 시간 포맷
                await alert_channel.send(
                    f"📌 **{member.mention}**님이 `{self.study_channel_name}`에서 공부를 시작했다 삐!"
                    f"(`{now} KST`)"
                )

        # ✅ 사용자가 '공부방'에서 나가거나 다른 채널로 이동한 경우
        elif before.channel and before.channel.name == self.study_channel_name and (after.channel != before.channel):
            # 저장된 입장 시간 가져오기 (없으면 None)
            start_time = self.user_voice_times.pop(member.id, None)
            if start_time:
                end_time = datetime.now(self.kst)  # 퇴장 시간
                duration = end_time - start_time  # 공부한 전체 시간 (datetime.timedelta)
                minutes = int(duration.total_seconds() // 60)  # 분 단위로 환산

                # 텍스트 알림 채널 찾기
                if alert_channel:
                    await alert_channel.send(
                        f"✅ **{member.mention}**님이 `{self.study_channel_name}`에서 **퇴장**했다 삐!\n"
                        f"🕒 총 공부 시간: **{minutes}분**! {GoodJobMessage.random()}"
                        f"({start_time.strftime('%H:%M')} ~ {end_time.strftime('%H:%M')} KST)"
                    )

# Cog 등록을 위한 필수 비동기 setup 함수
async def setup(bot):
    await bot.add_cog(StudyTracker(bot))
