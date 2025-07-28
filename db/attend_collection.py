import dataclasses
from datetime import datetime

from db.client import db
from models.attend_model import AttendModel
from utils.time_utils import get_study_day_range


class AttendCollection:
    _collection = db["attend"]

    @classmethod
    async def insert_attend(cls, user_id: str, attend_time: datetime) -> str:
        """출석 시간을 데이터베이스에 삽입합니다."""

        attend_model = AttendModel(user_id=user_id, attend_time=attend_time)
        result = await cls._collection.insert_one(dataclasses.asdict(attend_model))
        return str(result.inserted_id)

    @classmethod
    async def get_today_user_is_attend(cls, user_id: str) -> bool:
        start_of_today, end_of_today = get_study_day_range(datetime.now())

        count = await cls._collection.count_documents(
            {
                "user_id": user_id,
                "attend_time": {"$gte": start_of_today, "$lt": end_of_today},
            }
        )

        return count > 0
