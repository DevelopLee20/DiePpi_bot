import dataclasses
from datetime import datetime

from db.client import db
from models.study_model import StudyModel


class StudyCollection:
    _collection = db["study"]

    @classmethod
    async def insert_study(cls, study: StudyModel) -> str:
        insert_model = dataclasses.asdict(study)
        result = await cls._collection.insert_one(insert_model)
        return str(result.inserted_id)

    @classmethod
    async def find_total_study_min_in_today(cls, user_id: str) -> int:
        today = datetime.now().date()
        start_of_today = datetime.combine(today, datetime.min.time())
        end_of_today = datetime.combine(today, datetime.max.time())

        total_time = await cls._collection.aggregate(
            [
                {
                    "$match": {
                        "user_id": user_id,
                        "start_time": {"$gte": start_of_today, "$lt": end_of_today},
                    }
                },
                {"$group": {"_id": None, "total_min": {"$sum": "$total_min"}}},
            ]
        ).to_list(length=None)

        return total_time[0]["total_min"] if total_time else 0
