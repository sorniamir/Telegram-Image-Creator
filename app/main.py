from fastapi import FastAPI

app = FastAPI(title="Telegram Manager")


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "telegram-manager"
    }


@app.get("/health")
async def health():
    return {
        "ok": True
    }
