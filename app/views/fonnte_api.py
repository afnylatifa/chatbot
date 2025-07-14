import os
import httpx
from dotenv import load_dotenv

load_dotenv()
FONNTE_TOKEN = os.getenv("FONNTE_TOKEN", "").strip()

if not FONNTE_TOKEN:
    raise ValueError("❌ Token Fonnte tidak ditemukan. Pastikan .env berisi FONNTE_TOKEN.")

async def kirim_balasan_ke_whatsapp(nomor: str, pesan: str):
    url = "https://api.fonnte.com/send"
    headers = {
        "Authorization": FONNTE_TOKEN
    }
    payload = {
        "target": nomor,
        "message": pesan,
        "delay": 1,
        "countryCode": "62"
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, data=payload)
