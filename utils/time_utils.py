from datetime import datetime, time, timedelta


def min_to_hhmm_str(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}시간 {mins}분" if hours > 0 else f"{mins}분"


def get_study_day_range(time_now: datetime) -> tuple[datetime, datetime]:
    start_day = time_now.date()

    # 새벽 4시 이전일 때, 전날 기준으로 처리
    if time_now.hour < 4:
        start_day -= timedelta(days=1)

    start_time = datetime.combine(start_day, time(4, 0))
    end_time = start_time + timedelta(days=1)

    return start_time, end_time
