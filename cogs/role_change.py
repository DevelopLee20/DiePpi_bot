import discord
from discord.ext import commands

from core.enums import Mode, Role
from core.env import env
from core.messages import upgrade_role_message
from db.study_collection import StudyCollection


class RoleChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if env.MODE == Mode.PROD.value:
            print("☑️ PROD mode.")
            self.study_channel_name = "공부방"
            self.alert_channel_name = "스터디-알림"
        else:
            print("☑️ DEV mode.")
            self.study_channel_name = "디스코드-봇-만드는-채널"
            self.alert_channel_name = "디스코드-봇-만드는-채널"

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild

        alert_channel = discord.utils.get(
            guild.text_channels, name=self.alert_channel_name
        )

        total_study_min = await StudyCollection.find_total_study_min_in_today(
            str(member.id)
        )

        if total_study_min > 180:
            role = discord.utils.get(
                guild.roles, name=Role.DEVELOPMENT_FAIRY.value
            )  # 개발 요정 역할
            if role and role not in member.roles:
                await member.add_roles(role)
                await alert_channel.send(
                    upgrade_role_message(member.mention, role.name)
                )


async def setup(bot):
    await bot.add_cog(RoleChange(bot))
