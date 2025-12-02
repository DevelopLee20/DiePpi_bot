import dataclasses
import logging
from datetime import datetime

from db.client import db
from models.study_model import StudyModel
from utils.time_utils import get_study_day_range, get_weekly_date_range

logger = logging.getLogger(__name__)


class StudyCollection:
    _collection = db["study"]

    @classmethod
    async def insert_study(cls, study: StudyModel) -> str:
        try:
            insert_model = dataclasses.asdict(study)
            result = await cls._collection.insert_one(insert_model)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(
                f"공부 기록 삽입 실패 (user_id={study.user_id}): {e}", exc_info=True
            )
            raise

    @classmethod
    async def insert_multiple_studies(cls, studies: list[StudyModel]) -> list[str]:
        """여러 공부 기록을 한 번에 삽입합니다 (시간 분할 시 사용).

        Args:
            studies: 삽입할 공부 기록 리스트

        Returns:
            삽입된 문서들의 ID 리스트
        """
        try:
            if not studies:
                return []

            insert_models = [dataclasses.asdict(study) for study in studies]
            result = await cls._collection.insert_many(insert_models)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(
                f"공부 기록 일괄 삽입 실패 (count={len(studies)}): {e}", exc_info=True
            )
            raise

    @classmethod
    async def find_total_study_min_in_today(cls, user_id: str) -> int:
        """오늘 오전 6시부터 다음날 오전 6시까지의 총 공부시간을 계산합니다.
        Args:
            user_id (str): 사용자의 ID
        Returns:
            int: 오늘 오전부터 다음날 오전 6시까지의 총 공부시간 (분 단위)
        """
        try:
            start_of_today, end_of_today = get_study_day_range(datetime.now())

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
        except Exception as e:
            logger.error(
                f"총 공부 시간 조회 실패 (user_id={user_id}): {e}", exc_info=True
            )
            raise

    @classmethod
    async def get_yesterday_top_rankings(cls, limit: int = 3) -> list[dict]:
        """어제(어제 오전 6시 ~ 오늘 오전 6시)의 공부 시간 순위를 반환합니다.

        Args:
            limit (int): 반환할 상위 순위 개수 (기본값: 3)

        Returns:
            list[dict]: [{"user_id": str, "total_min": int}, ...] 형태의 순위 리스트
        """
        try:
            from datetime import timedelta

            # 어제의 범위 계산 (어제 오전 6시 ~ 오늘 오전 6시)
            yesterday = datetime.now() - timedelta(days=1)
            start_of_yesterday, end_of_yesterday = get_study_day_range(yesterday)

            rankings = await cls._collection.aggregate(
                [
                    {
                        "$match": {
                            "start_time": {
                                "$gte": start_of_yesterday,
                                "$lt": end_of_yesterday,
                            },
                        }
                    },
                    {
                        "$group": {
                            "_id": "$user_id",
                            "total_min": {"$sum": "$total_min"},
                        }
                    },
                    {"$sort": {"total_min": -1}},
                    {"$limit": limit},
                    {"$project": {"_id": 0, "user_id": "$_id", "total_min": 1}},
                ]
            ).to_list(length=None)

            return rankings
        except Exception as e:
            logger.error(f"어제 공부 순위 조회 실패: {e}", exc_info=True)
            raise

    @classmethod
    async def get_weekly_study_by_user(cls, user_id: str) -> list[dict]:
        """사용자의 주간(일요일~토요일) 공부 시간을 요일별로 반환합니다.

        Args:
            user_id: 사용자 ID

        Returns:
            list[dict]: [{"day_name": "일", "total_min": 300}, ...] 형태의 7개 요일 데이터
        """
        try:
            weekly_ranges = get_weekly_date_range(datetime.now())

            result = []
            for start_time, end_time, day_name in weekly_ranges:
                total_time = await cls._collection.aggregate(
                    [
                        {
                            "$match": {
                                "user_id": user_id,
                                "start_time": {"$gte": start_time, "$lt": end_time},
                            }
                        },
                        {"$group": {"_id": None, "total_min": {"$sum": "$total_min"}}},
                    ]
                ).to_list(length=None)

                total_min = total_time[0]["total_min"] if total_time else 0
                result.append({"day_name": day_name, "total_min": total_min})

            return result
        except Exception as e:
            logger.error(
                f"주간 공부 시간 조회 실패 (user_id={user_id}): {e}", exc_info=True
            )
            raise
