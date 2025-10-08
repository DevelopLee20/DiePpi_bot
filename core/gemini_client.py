import logging

from google import genai
from google.genai import types

from core.env import env

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini AI API와 상호작용하는 클라이언트."""

    def __init__(self, instruction: str) -> None:
        """GeminiClient 초기화.

        Args:
            instruction: Gemini 모델에 전달할 시스템 instruction
        """
        self.client: genai.Chat | None = None
        self.instruction: str = instruction

    async def initialize(self) -> None:
        """Gemini 클라이언트를 초기화합니다."""
        client = genai.Client(api_key=env.GEMINI_API_KEY)

        gemini_chat = client.chats.create(
            model=env.GEMINI_MODEL,
            config=types.GenerateContentConfig(system_instruction=self.instruction),
        )

        self.client = gemini_chat

    async def create_gemini_message(self, input_word: str) -> tuple[bool, str]:
        """Gemini에게 메시지를 전송하고 응답을 받습니다.

        Args:
            input_word: Gemini에게 보낼 입력 텍스트

        Returns:
            (성공 여부, 응답 텍스트) 튜플
        """
        if self.client is None:
            await self.initialize()
        try:
            return True, self.client.send_message(input_word).text
        except TimeoutError as e:
            logger.error(f"GEMINI 응답 시간 초과: {e}")
            return False, f"GEMINI 응답 시간 초과: {e}"
        except ConnectionError as e:
            logger.error(f"GEMINI 연결 오류: {e}")
            return False, f"GEMINI 연결 오류: {e}"
        except ValueError as e:
            logger.error(f"GEMINI 입력 오류: {e}")
            return False, f"GEMINI 입력 오류: {e}"
        except Exception as e:
            logger.error(f"GEMINI 예상치 못한 오류: {e}", exc_info=True)
            return False, f"GEMINI 오류 발생: {e}"
