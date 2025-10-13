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
