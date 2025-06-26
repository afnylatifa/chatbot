from fastapi import APIRouter, Request
from app.views.response_templates import get_stateful_response
import httpx
import os
from dotenv import load_dotenv

router = APIRouter()

# Load token dari .env
FONNTE_TOKEN = "PaeFfyiPT88Qnetakyc2"

if not FONNTE_TOKEN:
    raise ValueError("❌ Token Fonnte tidak ditemukan. Pastikan .env berisi FONNTE_TOKEN.")
else:
    FONNTE_TOKEN = FONNTE_TOKEN.strip()  # Buang karakter aneh seperti \r\n

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
        response = await client.post(url, headers=headers, data=payload)
        print("📤 BALAS KE WA:", response.status_code, response.text)

# Endpoint webhook yang menerima request dari Fonnte
@router.post("/")
async def fonnte_webhook(request: Request):
    data = await request.json()
    print("🔵 DATA MASUK:", data)

    # Ambil pengirim dan isi pesan
    user_id = data.get("pengirim") or data.get("sender")
    pesan = data.get("pesan") or data.get("message")

    if not user_id or not pesan:
        print("🔴 DATA TIDAK VALID")
        return {"message": "Data tidak valid. Pastikan format berisi pengirim dan pesan."}

    # Proses balasan chatbot
    balasan = get_stateful_response(user_id, pesan)
    print("🟢 BALASAN:", balasan)

    # Kirim balasan ke WhatsApp via Fonnte
    await kirim_balasan_ke_whatsapp(user_id, balasan)

    return {"message": "OK"}
