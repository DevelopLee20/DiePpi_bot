"""출석 관련 데이터베이스 컬렉션 테스트"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from db.attend_collection import AttendCollection


class TestAttendCollection:
    """AttendCollection 클래스 테스트"""

    @pytest.mark.asyncio
    async def test_get_today_attended_user_ids_empty(self):
        """출석한 유저가 없는 경우"""
        mock_cursor = MagicMock()
        mock_cursor.to_list = AsyncMock(return_value=[])

        with patch.object(
            AttendCollection._collection, "find", return_value=mock_cursor
        ):
            result = await AttendCollection.get_today_attended_user_ids()

            assert result == []
            assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_get_today_attended_user_ids_single_user(self):
        """한 명의 유저가 출석한 경우"""
        mock_records = [{"user_id": "123456"}]
        mock_cursor = MagicMock()
        mock_cursor.to_list = AsyncMock(return_value=mock_records)

        with patch.object(
            AttendCollection._collection, "find", return_value=mock_cursor
        ):
            result = await AttendCollection.get_today_attended_user_ids()

            assert result == ["123456"]
            assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_today_attended_user_ids_multiple_users(self):
        """여러 유저가 출석한 경우"""
        mock_records = [
            {"user_id": "123456"},
            {"user_id": "789012"},
            {"user_id": "345678"},
        ]
        mock_cursor = MagicMock()
        mock_cursor.to_list = AsyncMock(return_value=mock_records)

        with patch.object(
            AttendCollection._collection, "find", return_value=mock_cursor
        ):
            result = await AttendCollection.get_today_attended_user_ids()

            assert len(result) == 3
            assert "123456" in result
            assert "789012" in result
            assert "345678" in result

    @pytest.mark.asyncio
    async def test_get_today_attended_user_ids_duplicate_users(self):
        """같은 유저가 여러 번 출석 기록이 있는 경우 (중복 제거)"""
        mock_records = [
            {"user_id": "123456"},
            {"user_id": "123456"},  # 중복
            {"user_id": "789012"},
        ]
        mock_cursor = MagicMock()
        mock_cursor.to_list = AsyncMock(return_value=mock_records)

        with patch.object(
            AttendCollection._collection, "find", return_value=mock_cursor
        ):
            result = await AttendCollection.get_today_attended_user_ids()

            assert len(result) == 2  # 중복 제거되어 2개
            assert "123456" in result
            assert "789012" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
