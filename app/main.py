from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uvicorn

from repository import SQLiteEmailDatabase, DynamoDBEmailDatabase, EmailRepository

app = FastAPI()
# 사용할 데이터베이스 선택 (SQLite 또는 DynamoDB)
db_instance = DynamoDBEmailDatabase("real-estate-newsletter-email-table")  # 또는 SQLiteEmailDatabase("emails.db")

# EmailRepository 생성
def get_email_repository() -> EmailRepository:
    return EmailRepository(db_instance)


class Email(BaseModel):
    email: str



@app.post('/subscribe')
def subscribe_email(email: str, db: EmailRepository = Depends(get_email_repository)):
    db.save_email(email)
    print("email has been registered to our list " + email)


@app.post('/unsubscribe')
def unsubscribe_email(email: str,  db: EmailRepository = Depends(get_email_repository)):
    # TODO: check if the email exists in db
    db.remove_emails(email)
    print("email has been removed from our list " + email)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)