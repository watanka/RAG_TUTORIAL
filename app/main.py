from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post('/subscribe')
def subscribe_email(email: str):

    print("email has been registered to our list " + email)


@app.post('/unsubscribe')
def unsubscribe_email(email: str):
    print("email has been removed from our list " + email)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)