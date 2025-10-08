from motor.motor_asyncio import AsyncIOMotorClient

from core.env import env

# 비동기 클라이언트
client = AsyncIOMotorClient(env.MONGO_DB)

db = client["base"]


def close_db_connection():
    """DB 연결을 종료합니다."""
    client.close()
