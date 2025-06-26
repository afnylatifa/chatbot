from fastapi import FastAPI
from app.controllers.webhook_controller import router as webhook_router

app = FastAPI()

@app.get("/")
async def check():
    return {"status": "Webhook is running"}

app.include_router(webhook_router)
