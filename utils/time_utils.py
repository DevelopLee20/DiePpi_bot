def min_to_hhmm_str(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}시간 {mins}분" if hours > 0 else f"{mins}분"
