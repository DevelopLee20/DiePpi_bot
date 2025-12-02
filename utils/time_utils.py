from datetime import datetime, time, timedelta

# 공부 시간 집계 기준 시간 (오전 6시)
STUDY_DAY_START_HOUR = 6
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

    오전 6시부터 다음날 오전 6시까지를 하루로 간주합니다.
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


def get_weekly_date_range(date_now: datetime) -> list[tuple[datetime, datetime, str]]:
    """주간(일요일~토요일) 범위를 계산하고 각 날짜별 오전 6시 기준 시간 범위를 반환합니다.

    Args:
        date_now: 기준 날짜/시간

    Returns:
        [(start_time, end_time, day_name), ...] 리스트 (일요일부터 토요일까지 7개)
        각 범위는 해당 날짜 오전 6시 ~ 다음날 오전 6시
    """
    # 이번주의 일요일 찾기 (0 = 월요일, 6 = 일요일)
    today = date_now.date()
    days_since_sunday = (today.weekday() + 1) % 7  # 일요일 = 0
    sunday = today - timedelta(days=days_since_sunday)

    day_names = ["일", "월", "화", "수", "목", "금", "토"]
    result = []

    for i in range(7):
        day = sunday + timedelta(days=i)
        start = datetime.combine(day, time(STUDY_DAY_START_HOUR, 0))
        end = start + timedelta(days=1)
        result.append((start, end, day_names[i]))

    return result


def split_study_session_by_cutoff(
    start_time: datetime, end_time: datetime
) -> list[tuple[datetime, datetime, int]]:
    """공부 세션이 오전 6시를 넘어가면 전날과 오늘로 분할합니다.

    Args:
        start_time: 공부 시작 시간
        end_time: 공부 종료 시간

    Returns:
        [(start_time, end_time, minutes), ...] 리스트
        오전 6시를 넘지 않으면 1개, 넘으면 2개의 튜플 반환
    """
    # 오전 6시 기준 시간 계산
    cutoff_date = end_time.date()

    if start_time.hour < STUDY_DAY_CUTOFF_HOUR and start_time.date() == cutoff_date:
        cutoff_date = start_time.date()

    cutoff_time = datetime.combine(cutoff_date, time(STUDY_DAY_CUTOFF_HOUR, 0))

    # 오전 6시를 넘지 않는 경우
    if start_time >= cutoff_time or end_time <= cutoff_time:
        duration = end_time - start_time
        minutes = int(duration.total_seconds() // 60)
        return [(start_time, end_time, minutes)]

    # 오전 6시를 넘는 경우 - 전날과 오늘로 분할
    sessions = []

    # 전날 세션 (start_time ~ 오전 6시)
    prev_duration = cutoff_time - start_time
    prev_minutes = int(prev_duration.total_seconds() // 60)
    if prev_minutes > 0:
        sessions.append((start_time, cutoff_time, prev_minutes))

    # 오늘 세션 (오전 6시 ~ end_time)
    today_duration = end_time - cutoff_time
    today_minutes = int(today_duration.total_seconds() // 60)
    if today_minutes > 0:
        sessions.append((cutoff_time, end_time, today_minutes))

    return sessions
