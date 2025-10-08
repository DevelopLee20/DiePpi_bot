from dataclasses import dataclass

from core.env import env


@dataclass(frozen=True)
class BotConfig:
    """봇 설정을 관리하는 클래스"""

    study_channel: str
    alert_channel: str
    mode: str

    @classmethod
    def from_env(cls) -> "BotConfig":
        """환경변수로부터 Config 생성"""
        if env.MODE == "PROD":
            return cls(
                study_channel="공부방",
                alert_channel="스터디-알림",
                mode="PROD",
            )
        else:
            return cls(
                study_channel="디스코드-봇-만드는-채널",
                alert_channel="디스코드-봇-만드는-채널",
                mode="DEV",
            )
