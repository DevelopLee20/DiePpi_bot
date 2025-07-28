from core.random_messages import RandomMessageManager
from utils.time_utils import min_to_hhmm_str

rm_manager = RandomMessageManager()


def hello_message(mention: str) -> str:
    return f"{mention} {rm_manager.random_greeting_message()}"


def start_study_message(mention: str) -> str:
    return f"{mention}님이 공부를 시작했다 삐!"


def attend_study_message(mention: str) -> str:
    return f"{mention}님 출석체크 완료! 삐!"


def end_study_message(
    mention: str, minutes: int, total_minute: int, text: str, status: bool
) -> str:
    if not status:
        text = rm_manager.random_good_job_message()

    return (
        f"✅ **{mention}**님이 공부를 종료했다 삐!\n"
        f"🕒 공부 시간: **{min_to_hhmm_str(minutes)}**! \n"
        f"📊 오늘 누적 공부 시간: **{min_to_hhmm_str(total_minute)}**!\n{text}"
    )


def upgrade_role_message(mention: str, role_name: str) -> str:
    return f"🎉 **{mention}**님이 **{role_name}** 역할을 획득했다 삐! 축하한다 삐!"


def gemini_response_message(mention: str, response: str) -> str:
    return f"{mention} {response}"
