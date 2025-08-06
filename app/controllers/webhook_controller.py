from fastapi import APIRouter, Request
from datetime import datetime
import asyncio

from app.models.chat_model import get_stateful_response, user_state
from app.views.fonnte_api import kirim_balasan_ke_whatsapp

router = APIRouter()

# State yang akan diberikan reminder jika user diam
state_yang_perlu_callback = ["main_menu", "menu_ajukan", "syarat_pengajuan", "konfirmasi_kontak"]

async def kirim_callback_jika_diam(user_id: str, delay_detik: int = 300):
    await asyncio.sleep(delay_detik)

    data_user = user_state.get(user_id)
    if not data_user:
        return

    terakhir = data_user.get("last_active")
    state = data_user.get("state")

    # Hanya kirim callback kalau state masih termasuk yang diinginkan
    if state not in state_yang_perlu_callback:
        return

    if terakhir and (datetime.now() - terakhir).total_seconds() >= delay_detik:
        pesan_callback = "⏰ Anda masih di sana? Ketik *menu* untuk melanjutkan."
        await kirim_balasan_ke_whatsapp(user_id, pesan_callback)

@router.post("/")
async def fonnte_webhook(request: Request):
    data = await request.json()

    user_id = data.get("pengirim") or data.get("sender")
    pesan = data.get("pesan") or data.get("message")

    if not user_id or not pesan:
        return {"message": "Data tidak valid. Format harus berisi pengirim dan pesan."}

    # Buat balasan
    balasan = get_stateful_response(user_id, pesan)

    # Kirim ke WhatsApp
    await kirim_balasan_ke_whatsapp(user_id, balasan)

    # Jadwalkan callback jika user diam
    asyncio.create_task(kirim_callback_jika_diam(user_id, delay_detik=300))

    return {"message": "Balasan terkirim ke pengguna"}
