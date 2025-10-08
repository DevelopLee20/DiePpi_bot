import logging

import discord
from discord.ext import commands

from core.enums import Role
from core.messages import upgrade_role_message
from db.study_collection import StudyCollection
from utils.discord_utils import get_text_channel_by_name

logger = logging.getLogger(__name__)

# 역할 부여 기준 (분 단위)
ROLE_REQUIREMENTS = [
    (180, Role.DEVELOPMENT_FAIRY),
    (360, Role.SENIOR_FAIRY),
]


class RoleChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _assign_role_if_eligible(
        self,
        member: discord.Member,
        total_study_min: int,
        min_required: int,
        role_enum: Role,
        alert_channel: discord.TextChannel | None = None,
    ) -> None:
        """조건을 만족하면 역할을 부여합니다.

        Args:
            member: 역할을 부여할 멤버
            total_study_min: 총 공부 시간 (분)
            min_required: 필요한 최소 시간 (분)
            role_enum: 부여할 역할 Enum
            alert_channel: 알림을 보낼 채널
        """
        if total_study_min <= min_required:
            return

        guild = member.guild
        role = discord.utils.get(guild.roles, name=role_enum.value)

        if role is None:
            logger.error(f"역할 '{role_enum.value}'을 찾을 수 없습니다.")
            return

        if role in member.roles:
            return

        try:
            await member.add_roles(role)
            logger.info(f"{member.name}에게 '{role.name}' 역할 부여 완료")

            if alert_channel:
                await alert_channel.send(
                    upgrade_role_message(member.mention, role.name)
                )
        except discord.Forbidden:
            logger.error(f"{member.name}에게 역할 부여 권한이 없습니다.")
        except discord.HTTPException as e:
            logger.error(f"역할 부여 중 오류 발생: {e}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        config = self.bot.config

        alert_channel = get_text_channel_by_name(guild, config.alert_channel)

        try:
            total_study_min = await StudyCollection.find_total_study_min_in_today(
                str(member.id)
            )
        except Exception as e:
            logger.error(f"공부 시간 조회 실패: {e}")
            return

        # 역할 부여 조건 체크
        for min_required, role_enum in ROLE_REQUIREMENTS:
            await self._assign_role_if_eligible(
                member, total_study_min, min_required, role_enum, alert_channel
            )


async def setup(bot):
    await bot.add_cog(RoleChange(bot))
