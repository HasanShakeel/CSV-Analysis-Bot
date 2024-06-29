from fastapi import FastAPI
from endpoints import upload
from endpoints import chatbot
from endpoints import issueToken

app = FastAPI()
app.include_router(issueToken.app)
app.include_router(upload.app)
app.include_router(chatbot.app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
