from fastapi import APIRouter, Request
from app.models.chat_model import get_stateful_response
from app.views.fonnte_api import kirim_balasan_ke_whatsapp

router = APIRouter()

@router.post("/send")
async def fonnte_webhook(request: Request):
    data = await request.json()
    
    user_id = data.get("pengirim") or data.get("sender")
    pesan = data.get("pesan") or data.get("message")

    if not user_id or not pesan:
        return {"message": "Data tidak valid. Format harus berisi pengirim dan pesan."}
        
    balasan = get_stateful_response(user_id, pesan)
    
    await kirim_balasan_ke_whatsapp(user_id, balasan)
    return {"message": "Balasan terkirim ke pengguna"}
