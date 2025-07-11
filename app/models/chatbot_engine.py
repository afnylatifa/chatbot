from fastapi import FastAPI
from app.controllers.webhook_controller import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)
