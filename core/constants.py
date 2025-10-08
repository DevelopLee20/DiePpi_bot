"""애플리케이션 전역 상수를 정의하는 모듈."""

from core.enums import Role

# 역할 부여 기준 시간 (분 단위)
ROLE_REQUIREMENT_DEVELOPMENT_FAIRY_MIN = 180  # 3시간
ROLE_REQUIREMENT_SENIOR_FAIRY_MIN = 360  # 6시간

# 역할 요구사항 (분, 역할) 튜플 리스트
DEFAULT_ROLE_REQUIREMENTS: list[tuple[int, Role]] = [
    (ROLE_REQUIREMENT_DEVELOPMENT_FAIRY_MIN, Role.DEVELOPMENT_FAIRY),
    (ROLE_REQUIREMENT_SENIOR_FAIRY_MIN, Role.SENIOR_FAIRY),
]
