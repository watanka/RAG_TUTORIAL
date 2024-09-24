# 베이스 이미지 설정
FROM python:3.12-slim


COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

EXPOSE 8000
# 앱 실행
CMD ["python", "main.py"]