# 베이스 이미지 설정
FROM python:3.12-slim

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 의존성 목록을 복사
COPY pyproject.toml poetry.lock* /app/

# Poetry 설치
RUN pip install poetry

# 의존성 설치
RUN poetry install --no-dev

# 애플리케이션 코드 복사
COPY . .

# FastAPI 앱 실행
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]