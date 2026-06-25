from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "Healthy!\n"


@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "Pong!\n"
