# scheduled/Dockerfile
FROM python:3.12-slim


# 의존성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 스케줄러 실행
CMD ["python", "main.py"]