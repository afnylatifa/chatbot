import json

user_state = {}

# Load dataset sekali di awal
with open("app/dataset/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

def dengan_footer(pesan_utama: str, state: str = "", q: list[str] = None) -> str:
    if q is None:
        q = []

    if state == "main_menu" and q == ["1"]:
        footer = "\n\n🟢 *Ketik angka pilihan Anda* (misal: `1`), atau ketik `selesai` untuk keluar dari chatbot."
    elif state == "menu_ajukan" and q == ["1"]:
        footer = "\n\n🟢 *Ketik angka pilihan Anda* (misal: `1`), atau ketik `selesai` untuk keluar dari chatbot."
    elif state == "main_menu" and q == ["5"]:
        footer = ""
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

    # Atur state awal jika belum ada
    if user_id not in user_state:
        user_state[user_id] = {"state": "main_menu"}

    state = user_state[user_id]["state"]

    # Jika user minta menu atau sapaan
    if pesan in help_menu or pesan in greetings:
        user_state[user_id] = {
            "state": "main_menu",
            "q": ["1"]
        }
        return dengan_footer(
            "👋 Hai, selamat datang di Chatbot Desa Limapoccoe!\n"
            "Ada yang bisa kami bantu hari ini? Silakan pilih menu yang tersedia, ya 😊\n"
            "1. Ajukan Surat\n"
            "2. Pengaduan\n"
            "3. Jadwal Posyandu\n"
            "4. Jam Operasional\n"
            "5. Hubungi Petugas",
            "main_menu",
            ["1"]
        )

    # Keluar dari sesi
    if pesan in exit_commands:
        user_state[user_id]["state"] = "main_menu"
        return "✅ Sesi diakhiri. Ketik *menu* untuk mulai lagi."

    # Ucapan terima kasih
    if pesan in thanks:
        return "🙏 Sama-sama!"

    # ⛔ Blokir input angka (1–5) jika user tidak berada di state yang seharusnya
    if pesan in ["1", "2", "3", "4", "5"] and state not in ["main_menu", "menu_ajukan", "syarat_pengajuan", "konfirmasi_kontak"]:
        return "❓ Maaf, pilihan tidak dikenali. Ketik *menu* untuk kembali ke menu utama."

    # 🔍 Cari jawaban dari dataset berdasarkan state dan pesan
    jawaban, next_state = cari_dari_dataset(state, pesan)
    if jawaban:
        if next_state:
            user_state[user_id]["state"] = next_state
        return dengan_footer(jawaban, state, [pesan])

    return "❓ Maaf, pilihan tidak dikenali. Ketik *menu* untuk kembali ke menu utama."
