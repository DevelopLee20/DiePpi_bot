import discord
from discord.ext import commands

from core.enums import Role
from core.messages import upgrade_role_message
from db.study_collection import StudyCollection
from main import ALERT_CHANNEL


class RoleChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild

        alert_channel = discord.utils.get(guild.text_channels, name=ALERT_CHANNEL)

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

        if total_study_min > 360:
            role = discord.utils.get(
                guild.roles, name=Role.SENIOR_FAIRY.value
            )  # 시니어 요정 역할
            if role and role not in member.roles:
                await member.add_roles(role)
                await alert_channel.send(
                    upgrade_role_message(member.mention, role.name)
                )


async def setup(bot):
    await bot.add_cog(RoleChange(bot))
