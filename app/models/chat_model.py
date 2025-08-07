import json
from datetime import datetime

# Daftar kata ucapan terima kasih
thanks = [
    "terima kasih", "terimakasih", "makasih", "makasi",
    "thanks", "thank you", "trimakasih", "trims"
]

# Callback untuk balasan terima kasih
def balas_terimakasih():
    return "🙏 Sama-sama!"

# Menyimpan state pengguna
user_state = {}

# Membaca data dari dataset.json
with open("app/dataset/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Menambahkan footer jika tersedia
def dengan_footer(pesan_utama: str, state: str = "", q: list[str] = None) -> str:
    if q is None:
        q = []

    for item in dataset:
        if item.get("state") == state and item.get("q") == q:
            footer = item.get("footer")
            if footer is not None:
                return f"{pesan_utama}\n\n{footer}" if footer else pesan_utama
    return pesan_utama

# Cari respons dari dataset
def cari_dari_dataset(state: str, pesan: str):
    pesan = pesan.lower()

    for item in dataset:
        if item.get("state") == state or item.get("state") == "*":
            for q in item.get("q", []):
                if pesan == q.lower():
                    return item.get("a"), item.get("next_state"), item.get("q"), item.get("state")

    # Fallback jika tidak ditemukan
    for item in dataset:
        if item.get("state") == "*" and "__fallback__" in item.get("q", []):
            return item.get("a"), None, item.get("q"), item.get("state")

    return None, None, None, None

# Fungsi utama untuk menghasilkan respons chatbot
def get_stateful_response(user_id: str, pesan: str) -> str:
    pesan = pesan.strip().lower()

    # ⏱️ Inisialisasi state awal
    if user_id not in user_state:
        user_state[user_id] = {
            "state": "main_menu",
            "last_active": datetime.now()
        }
    else:
        user_state[user_id]["last_active"] = datetime.now()

    # ✅ Tangani ucapan terima kasih sebagai callback khusus (global, di luar state)
    if pesan in thanks:
        return balas_terimakasih()

    # 🚀 Lanjut ke pemrosesan berbasis state
    state = user_state[user_id]["state"]
    jawaban, next_state, matched_q, matched_state = cari_dari_dataset(state, pesan)

    # 🔁 Perbarui state jika perlu
    if next_state:
        user_state[user_id]["state"] = next_state
    elif state in ["syarat_pengajuan", "main_menu"]:
        user_state[user_id]["state"] = "done"

    return dengan_footer(jawaban or "❓ Maaf, pilihan tidak dikenali.", matched_state, matched_q)
