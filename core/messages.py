from core.random_messages import RandomMessageManager
from utils.time_utils import min_to_hhmm_str

random_message_manager = RandomMessageManager()


def hello_message(mention: str) -> str:
    return f"{mention} {random_message_manager.random_greeting_message()}"


def start_study_message(mention: str) -> str:
    return f"{mention}님이 공부를 시작했다 삐!"


def attend_study_message(mention: str) -> str:
    return f"{mention}님 출석체크 완료! 삐!"


def end_study_message(
    mention: str,
    minutes: int,
    total_minute: int,
    text: str,
    status: bool,
    prev_day_total: int | None = None,
) -> str:
    if not status:
        text = random_message_manager.random_good_job_message()

    message = (
        f"✅ **{mention}**님이 공부를 종료했다 삐!\n"
        f"🕒 공부 시간: **{min_to_hhmm_str(minutes)}**! \n"
    )

    # 전날 누적시간이 있으면 (오전 6시를 넘어간 경우)
    if prev_day_total is not None:
        message += f"📊 전날 누적: **{min_to_hhmm_str(prev_day_total)}**, 오늘 누적: **{min_to_hhmm_str(total_minute)}**!\n"
    else:
        message += f"📊 오늘 누적 공부 시간: **{min_to_hhmm_str(total_minute)}**!\n"

    message += text
    return message


def upgrade_role_message(mention: str, role_name: str) -> str:
    return f"🎉 **{mention}**님이 **{role_name}** 역할을 획득했다 삐! 축하한다 삐!"


def gemini_response_message(mention: str, response: str) -> str:
    return f"{mention} {response}"


def study_encouragement_message(target_mention: str) -> str:
    return f"{target_mention}도 어서 들어오라고 삐!"


def yesterday_ranking_message(rankings: list[tuple[str, int]]) -> str:
    """어제의 공부 순위 메시지를 생성합니다.

    Args:
        rankings: [(user_mention, total_minutes), ...] 형태의 순위 리스트

    Returns:
        포맷된 순위 메시지
    """
    if not rankings:
        return "📊 어제 공부 기록이 없다 삐!"

    message = "📊 **어제의 공부 순위 TOP3** 삐!\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for idx, (user_mention, total_min) in enumerate(rankings):
        medal = medals[idx] if idx < len(medals) else f"{idx + 1}."
        time_str = min_to_hhmm_str(total_min)
        message += f"{medal} {user_mention}: **{time_str}**\n"

    return message


def weekly_stats_message(
    member_name: str, daily_stats: list[dict], total_min: int, evaluation: str
) -> str:
    """주간 공부 통계 메시지를 생성합니다.

    Args:
        member_name: 사용자 이름
        daily_stats: [{"day_name": "일", "total_min": 300}, ...] 형태의 7개 요일 데이터
        total_min: 주간 총 공부 시간 (분)
        evaluation: Gemini API로부터 받은 평가 메시지

    Returns:
        포맷된 주간 통계 메시지
    """
    message = f"📊 **{member_name}**님의 주간 공부 통계\n"
    message += "=" * 30 + "\n"

    for day_stat in daily_stats:
        day_name = day_stat["day_name"]
        min_val = day_stat["total_min"]
        time_str = min_to_hhmm_str(min_val)
        message += f"{day_name}: {time_str}\n"

    message += "=" * 30 + "\n"
    total_str = min_to_hhmm_str(total_min)
    message += f"**합계: {total_str}**\n\n"

    message += f"**죽어삐의 한마디:** {evaluation}"

    return message
