from pydantic_settings import BaseSettings

class Env(BaseSettings):
    TOKEN: str
    
    class Config:
        env_file = ".env"

env = Env()
