# DiePpi_bot

## 적용된 기능

```shell
1. 스터디 타이머 기능
   - 음성 채널 입장/퇴장 자동 감지
   - 오전 6시 기준 누적 시간 집계
   - 오전 6시를 넘어가는 세션 자동 분할 (전날/오늘 누적 시간 분리)
2. 출석 체크 기능
   - 최초 1회 자동 출석 체크
3. 공부 시간 기반 역할 자동 부여
4. 안녕! 인사해주는 기능
5. 잼민이(Gemini) 단어 뜻 알려주는 기능
```

## Start

```bash
poetry run poe start
```

또는

```bash
poetry run python main.py
```

## Development

### 테스트 실행

```bash
# 모든 테스트 실행
poetry run pytest

# 상세한 출력과 함께 테스트 실행
poetry run pytest -v

# 특정 파일만 테스트
poetry run pytest tests/test_time_utils.py -v
```

### Pre-commit

```bash
# Pre-commit 훅 설치 (최초 1회)
pre-commit install

# 모든 파일에 대해 pre-commit 실행
pre-commit run --all-files

# 특정 파일만 검사
pre-commit run --files <파일경로>
```
