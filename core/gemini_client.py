from google import genai
from google.genai import types

from core.env import env


class GeminiClient:
    def __init__(self, instruction: str):
        self.client = None
        self.instruction = instruction

    async def initialize(self):
        client = genai.Client(api_key=env.GEMINI_API_KEY)

        gemini_chat = client.chats.create(
            model="gemini-2.0-flash-lite",
            config=types.GenerateContentConfig(system_instruction=self.instruction),
        )

        self.client = gemini_chat

    async def create_gemini_message(self, input_word: str) -> tuple[bool, str]:
        if self.client is None:
            await self.initialize()
        try:
            return True, self.client.send_message(input_word).text
        except Exception as e:
            return False, f"GEMINI 오류 발생: {e}"
