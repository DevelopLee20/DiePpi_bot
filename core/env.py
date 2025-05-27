from pydantic_settings import BaseSettings


class Env(BaseSettings):
    TOKEN: str
    MONGO_DB: str

    class Config:
        env_file = ".env"


env = Env()
