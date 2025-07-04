from fastapi import APIRouter, Request
from app.views.response_templates import get_stateful_response, user_state
import httpx
import os
from dotenv import load_dotenv

router = APIRouter()

# Load token dari .env
load_dotenv()
FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")

if not FONNTE_TOKEN:
    raise ValueError("❌ Token Fonnte tidak ditemukan. Pastikan .env berisi FONNTE_TOKEN.")
else:
    FONNTE_TOKEN = FONNTE_TOKEN.strip()

# Fungsi kirim pesan ke WhatsApp via API Fonnte
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

# Endpoint webhook yang menerima request dari Fonnte
@router.post("/")
async def fonnte_webhook(request: Request):
    data = await request.json()

    # Ambil pengirim dan isi pesan
    user_id = data.get("pengirim") or data.get("sender")
    pesan = data.get("pesan") or data.get("message")

    if not user_id or not pesan:
        print("🔴 DATA TIDAK VALID")
        return {"message": "Data tidak valid. Pastikan format berisi pengirim dan pesan."}

    # Proses balasan chatbot
    balasan = get_stateful_response(user_id, pesan)

    # Kirim balasan ke WhatsApp via Fonnte
    await kirim_balasan_ke_whatsapp(user_id, balasan)
    return {"message": "Balasan terkirim ke pengguna"}
