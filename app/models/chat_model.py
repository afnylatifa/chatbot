import json

user_state = {}

with open("app/dataset/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

def dengan_footer(pesan_utama: str, state: str = "", q: list[str] = None) -> str:
    if q is None:
        q = []

    for item in dataset:
        if item.get("state") == state and item.get("q") == q:
            footer = item.get("footer")
            if footer is not None:
                return f"{pesan_utama}\n\n{footer}" if footer else pesan_utama

def cari_dari_dataset(state: str, pesan: str):
    pesan = pesan.lower()
    for item in dataset:
        if item.get("state") == state or item.get("state") == "*":
            for q in item.get("q", []):
                if pesan == q.lower():
                    return item.get("a"), item.get("next_state"), item.get("q"), item.get("state")
    # Jika tidak ketemu, coba cari __fallback__
    for item in dataset:
        if item.get("state") == "*" and "__fallback__" in item.get("q", []):
            return item.get("a"), None, item.get("q"), item.get("state")
    return None, None, None, None


def get_stateful_response(user_id: str, pesan: str) -> str:
    pesan = pesan.strip().lower()

    if user_id not in user_state:
        user_state[user_id] = {"state": "main_menu"}

    state = user_state[user_id]["state"]

    # Tangani input dari user
    jawaban, next_state, matched_q, matched_state = cari_dari_dataset(state, pesan)
    if jawaban:
        if next_state:
            user_state[user_id]["state"] = next_state
        else:
            if state in ["syarat_pengajuan", "main_menu"]:
                user_state[user_id]["state"] = "done"
        return dengan_footer(jawaban, matched_state, matched_q)

    # Fallback jika tidak ditemukan
    fallback, _, matched_q, matched_state = cari_dari_dataset("*", "__fallback__")
    if fallback:
        return dengan_footer(fallback, matched_state, matched_q)
    else:
        return "❓ Maaf, pilihan tidak dikenali. Ketik *menu* untuk kembali ke menu utama."

