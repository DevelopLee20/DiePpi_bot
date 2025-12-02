from pydantic_settings import BaseSettings

from core.enums import Mode


class Env(BaseSettings):
    TOKEN: str
    MONGO_DB: str
    MODE: Mode
    GEMINI_API_KEY: str
    DB_NAME: str = "base"
    GEMINI_MODEL: str
    GEMINI_WORD_SEARCH_INSTRUCTION: str
    GEMINI_STUDY_ENCOURAGEMENT_INSTRUCTION: str
    GEMINI_WEEKLY_EVALUATION_INSTRUCTION: str
    COMMAND_PREFIX: str = "/"

    class Config:
        env_file = ".env"


env = Env()
