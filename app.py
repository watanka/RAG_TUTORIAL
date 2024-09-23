from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post('/subscribe')
def subscribe_email(email: str):

    print("email has been registered to our list " + email)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)