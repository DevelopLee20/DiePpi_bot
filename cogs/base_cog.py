import logging

import discord
from discord.ext import commands

from utils.discord_utils import get_text_channel_by_name

logger = logging.getLogger(__name__)


class BaseCog(commands.Cog):
    """공통 기능을 제공하는 Base Cog 클래스."""

    def __init__(self, bot: commands.Bot) -> None:
        """BaseCog 초기화.

        Args:
            bot: Discord bot 인스턴스
        """
        self.bot = bot

    def get_alert_channel(self, guild: discord.Guild) -> discord.TextChannel | None:
        """설정된 알림 채널을 반환합니다.

        Args:
            guild: Discord 서버 객체

        Returns:
            알림 채널 객체, 없으면 None
        """
        config = self.bot.config
        return get_text_channel_by_name(guild, config.alert_channel)
