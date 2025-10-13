import dataclasses
import logging
from datetime import datetime

from db.client import db
from models.attend_model import AttendModel
from utils.time_utils import get_study_day_range

logger = logging.getLogger(__name__)


class AttendCollection:
    _collection = db["attend"]

    @classmethod
    async def insert_attend(cls, user_id: str, attend_time: datetime) -> str:
        """출석 시간을 데이터베이스에 삽입합니다."""
        try:
            attend_model = AttendModel(user_id=user_id, attend_time=attend_time)
            result = await cls._collection.insert_one(dataclasses.asdict(attend_model))
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"출석 정보 삽입 실패 (user_id={user_id}): {e}", exc_info=True)
            raise

    @classmethod
    async def get_today_user_is_attend(cls, user_id: str) -> bool:
        try:
            start_of_today, end_of_today = get_study_day_range(datetime.now())

            count = await cls._collection.count_documents(
                {
                    "user_id": user_id,
                    "attend_time": {"$gte": start_of_today, "$lt": end_of_today},
                }
            )

            return count > 0
        except Exception as e:
            logger.error(f"출석 정보 조회 실패 (user_id={user_id}): {e}", exc_info=True)
            raise

    @classmethod
    async def get_today_attended_user_ids(cls) -> list[str]:
        """오늘 출석한 유저 ID 목록을 반환합니다."""
        try:
            start_of_today, end_of_today = get_study_day_range(datetime.now())

            # 오늘 출석한 유저들의 user_id를 조회
            cursor = cls._collection.find(
                {"attend_time": {"$gte": start_of_today, "$lt": end_of_today}},
                {"user_id": 1, "_id": 0},
            )

            records = await cursor.to_list(length=None)
            # 중복 제거하여 유저 ID 목록 반환
            return list({record["user_id"] for record in records})
        except Exception as e:
            logger.error(f"오늘 출석한 유저 목록 조회 실패: {e}", exc_info=True)
            raise
