import json

user_state = {}

# Load dataset sekali di awal
with open("app/dataset/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

def dengan_footer(pesan_utama: str, status: str = "pilih") -> str:
    if status == "pilih":
        footer = "\n\n🟢 *Ketik angka pilihan Anda* (misal: `1`), atau ketik `selesai` untuk keluar dari chatbot.*"
    else:
        footer = "\n\n🟢 Ketik *menu* untuk kembali atau *selesai* untuk keluar dari chatbot."
    return f"{pesan_utama}{footer}"

def cari_dari_dataset(state: str, pesan: str) -> tuple[str | None, str | None]:
    for item in dataset:
        if item.get("state") == state:
            for q in item.get("q", []):
                if pesan == q.lower():
                    return item.get("a"), item.get("next_state")
    return None, None

def get_stateful_response(user_id: str, pesan: str) -> str:
    pesan = pesan.strip().lower()

    greetings = ["halo", "hi", "hai", "assalamualaikum"]
    help_menu = ["menu", "panduan", "bantuan", "help"]
    exit_commands = ["selesai", "keluar", "akhiri", "stop", "end", "batal"]
    thanks = ["terima kasih", "makasih", "thanks", "thank you", "trimakasih", "trims"]

    # Atur state awal
    if user_id not in user_state:
        user_state[user_id] = {"state": "main_menu"}

    state = user_state[user_id]["state"]

    # 🔁 Reset ke menu utama
    if pesan in help_menu or pesan in greetings:
        user_state[user_id]["state"] = "main_menu"
        return dengan_footer(
            "👋 Selamat datang! Silakan pilih:\n"
            "1. Ajukan Surat\n"
            "2. Pengaduan\n"
            "3. Jam Operasional\n"
            "4. Hubungi Petugas"
        )

    if pesan in exit_commands:
        user_state[user_id]["state"] = "main_menu"
        return "✅ Sesi diakhiri. Ketik *menu* untuk mulai lagi."

    if pesan in thanks:
        return "🙏 Sama-sama! Ketik *menu* untuk pilihan lainnya."

    # 🔍 Cari jawaban berdasarkan state + input user
    jawaban, next_state = cari_dari_dataset(state, pesan)
    if jawaban:
        if next_state:
            user_state[user_id]["state"] = next_state
        return dengan_footer(jawaban)

    return "❓ Maaf, pilihan tidak dikenali. Ketik *menu* untuk kembali ke menu utama."
