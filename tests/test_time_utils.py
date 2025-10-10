"""시간 유틸리티 함수 테스트"""

from datetime import datetime

import pytest

from utils.time_utils import STUDY_DAY_CUTOFF_HOUR, split_study_session_by_cutoff


class TestSplitStudySessionByCutoff:
    """split_study_session_by_cutoff 함수 테스트"""

    def test_no_split_before_cutoff(self):
        """오전 6시 이전에만 공부한 경우 - 분할 없음"""
        # 오전 4시 ~ 5시 30분
        start = datetime(2025, 10, 11, 4, 0, 0)
        end = datetime(2025, 10, 11, 5, 30, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 1
        assert sessions[0][0] == start
        assert sessions[0][1] == end
        assert sessions[0][2] == 90  # 90분

    def test_no_split_after_cutoff(self):
        """오전 6시 이후에만 공부한 경우 - 분할 없음"""
        # 오전 7시 ~ 9시
        start = datetime(2025, 10, 11, 7, 0, 0)
        end = datetime(2025, 10, 11, 9, 0, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 1
        assert sessions[0][0] == start
        assert sessions[0][1] == end
        assert sessions[0][2] == 120  # 120분

    def test_split_crossing_cutoff(self):
        """오전 6시를 넘어가는 경우 - 분할됨"""
        # 오전 5시 ~ 7시 (6시를 넘어감)
        start = datetime(2025, 10, 11, 5, 0, 0)
        end = datetime(2025, 10, 11, 7, 0, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 2

        # 첫 번째 세션: 전날 (5시 ~ 6시)
        assert sessions[0][0] == start
        assert sessions[0][1] == datetime(2025, 10, 11, STUDY_DAY_CUTOFF_HOUR, 0, 0)
        assert sessions[0][2] == 60  # 60분

        # 두 번째 세션: 오늘 (6시 ~ 7시)
        assert sessions[1][0] == datetime(2025, 10, 11, STUDY_DAY_CUTOFF_HOUR, 0, 0)
        assert sessions[1][1] == end
        assert sessions[1][2] == 60  # 60분

    def test_split_crossing_cutoff_with_minutes(self):
        """오전 6시를 넘어가는 경우 - 분 단위까지 정확히 분할"""
        # 오전 5시 30분 ~ 6시 45분
        start = datetime(2025, 10, 11, 5, 30, 0)
        end = datetime(2025, 10, 11, 6, 45, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 2

        # 첫 번째 세션: 전날 (5시 30분 ~ 6시) = 30분
        assert sessions[0][2] == 30

        # 두 번째 세션: 오늘 (6시 ~ 6시 45분) = 45분
        assert sessions[1][2] == 45

        # 총 시간 확인
        total_minutes = sessions[0][2] + sessions[1][2]
        assert total_minutes == 75

    def test_split_long_session(self):
        """긴 시간 동안 공부한 경우"""
        # 오전 3시 ~ 10시 (7시간)
        start = datetime(2025, 10, 11, 3, 0, 0)
        end = datetime(2025, 10, 11, 10, 0, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 2

        # 첫 번째 세션: 전날 (3시 ~ 6시) = 180분
        assert sessions[0][2] == 180

        # 두 번째 세션: 오늘 (6시 ~ 10시) = 240분
        assert sessions[1][2] == 240

        # 총 시간 확인
        total_minutes = sessions[0][2] + sessions[1][2]
        assert total_minutes == 420  # 7시간

    def test_exactly_at_cutoff_start(self):
        """정확히 오전 6시에 시작한 경우"""
        # 오전 6시 ~ 8시
        start = datetime(2025, 10, 11, 6, 0, 0)
        end = datetime(2025, 10, 11, 8, 0, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 1
        assert sessions[0][2] == 120  # 120분

    def test_exactly_at_cutoff_end(self):
        """정확히 오전 6시에 끝난 경우"""
        # 오전 4시 ~ 6시
        start = datetime(2025, 10, 11, 4, 0, 0)
        end = datetime(2025, 10, 11, 6, 0, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 1
        assert sessions[0][2] == 120  # 120분

    def test_very_short_session_before_cutoff(self):
        """오전 6시 직전 짧은 세션"""
        # 오전 5시 55분 ~ 5시 59분
        start = datetime(2025, 10, 11, 5, 55, 0)
        end = datetime(2025, 10, 11, 5, 59, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 1
        assert sessions[0][2] == 4  # 4분

    def test_very_short_session_crossing_cutoff(self):
        """오전 6시를 짧게 넘는 세션"""
        # 오전 5시 58분 ~ 6시 2분
        start = datetime(2025, 10, 11, 5, 58, 0)
        end = datetime(2025, 10, 11, 6, 2, 0)

        sessions = split_study_session_by_cutoff(start, end)

        assert len(sessions) == 2

        # 첫 번째 세션: 5시 58분 ~ 6시 = 2분
        assert sessions[0][2] == 2

        # 두 번째 세션: 6시 ~ 6시 2분 = 2분
        assert sessions[1][2] == 2


if __name__ == "__main__":
    pytest.main(
        [__file__, "-v"]
    )  # __file__ : 현재 파일 경로, -v : 자세한 출력(verbose)
