import logging
from typing import Optional

import discord

logger = logging.getLogger(__name__)


def get_text_channel_by_name(
    guild: discord.Guild, channel_name: str
) -> Optional[discord.TextChannel]:
    """서버에서 텍스트 채널을 이름으로 찾습니다.

    Args:
        guild: 디스코드 서버 객체
        channel_name: 찾을 채널 이름

    Returns:
        찾은 채널 객체, 없으면 None
    """
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if channel is None:
        logger.warning(f"채널 '{channel_name}'을 찾을 수 없습니다.")
    return channel
