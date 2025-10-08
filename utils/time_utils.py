from datetime import datetime, time, timedelta

# 공부 시간 집계 기준 시간 (오전 4시)
STUDY_DAY_START_HOUR = 4
# 전날로 간주하는 기준 시간 (오전 6시 이전)
STUDY_DAY_CUTOFF_HOUR = 6


def min_to_hhmm_str(minutes: int) -> str:
    """분을 시간 형식 문자열로 변환합니다.

    Args:
        minutes: 분 단위 시간

    Returns:
        "N시간 M분" 또는 "M분" 형식의 문자열
    """
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}시간 {mins}분" if hours > 0 else f"{mins}분"


def get_study_day_range(time_now: datetime) -> tuple[datetime, datetime]:
    """공부 시간 집계를 위한 하루 범위를 계산합니다.

    오전 4시부터 다음날 오전 4시까지를 하루로 간주합니다.
    오전 6시 이전의 시간은 전날로 계산됩니다.

    Args:
        time_now: 기준 시간

    Returns:
        (시작 시간, 종료 시간) 튜플
    """
    start_day = time_now.date()

    # 새벽 6시 이전일 때, 전날 기준으로 처리
    if time_now.hour < STUDY_DAY_CUTOFF_HOUR:
        start_day -= timedelta(days=1)

    start_time = datetime.combine(start_day, time(STUDY_DAY_START_HOUR, 0))
    end_time = start_time + timedelta(days=1)

    return start_time, end_time
