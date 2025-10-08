import random


class RandomMessageManager:
    """랜덤한 인사말과 격려 메시지를 제공하는 관리자."""

    good_job_messages: list[str] = [
        "대단하다 삐!",
        "엄청나다 삐!",
        "미쳤다 삐!",
        "이제 좀 쉬어라 삐!",
        "반했다 삐!",
        "감탄했다 삐!",
        "이건 진짜 미쳤다 삐!!",
        "존경스럽다 삐… 진심으로!",
        "천재인가 삐?",
        "불났어 불났어, 실력이 불이야 삐!",
        "이건 충격이야 삐… 대체 어떻게 한 거야?",
        "장인이네 삐. 말이 필요 없다 삐.",
        "박수 짝짝짝!! 감동이다 삐!",
        "믿을 수가 없다 삐… 인간이야?",
        "영웅이 따로 없다 삐!",
        "차원이 다르다 삐! 렙업했네 삐!",
    ]

    greetings: list[str] = [
        "안녕하세요 삐! 만나서 반가워요!",
        "왔구나 삐! 기다리고 있었지!",
        "어서 오세요 삐~ 좋은 하루예요!",
        "왔다! 반가워요 삐!",
        "드디어 나타났군요 삐!",
        "하이하이~ 오늘도 빛나는 등장이다 삐!",
        "이 조용한 채널에 활기가 도는군요 삐!",
        "어이쿠! 누가 오셨나 삐? 반가워요!",
        "오늘도 열공인가요 삐? 환영해요!",
        "반가워요! 이제 시작해볼까요 삐?",
    ]

    @classmethod
    def random_good_job_message(cls) -> str:
        return random.choice(cls.good_job_messages)

    @classmethod
    def random_greeting_message(cls) -> str:
        return random.choice(cls.greetings)
