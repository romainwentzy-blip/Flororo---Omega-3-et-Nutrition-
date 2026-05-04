import os
import asyncio
from datetime import date
from telegram import Bot
from telegram.constants import ParseMode
from messages import MESSAGES

# ─── Variables d'environnement (à définir dans GitHub Secrets) ───────────────
BOT_TOKEN  = os.environ["TELEGRAM_BOT_TOKEN"]   # Token de ton bot @BotFather
CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]  # Ex: @flororo_omega3  ou  -100XXXXXXXXXX
START_DATE = os.environ.get("START_DATE", "2025-06-01")  # Date de début JJ-1 AAAA-MM-DD

# ─── Calcul du jour actuel ────────────────────────────────────────────────────
def get_current_day() -> int:
    start = date.fromisoformat(START_DATE)
    today = date.today()
    delta = (today - start).days + 1  # Jour 1 = date de début
    return delta

# ─── Envoi du message ─────────────────────────────────────────────────────────
async def post_daily_message():
    day = get_current_day()

    if day < 1 or day > 30:
        print(f"Jour {day} — hors du programme (1-30). Rien envoyé.")
        return

    message = next((m for m in MESSAGES if m["day"] == day), None)
    if not message:
        print(f"Jour {day} — message introuvable.")
        return

    bot = Bot(token=BOT_TOKEN)

    header = f"📅 <b>Jour {day}/30 — {message['topic']}</b>\n\n"
    full_text = header + message["text"]

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=full_text,
        parse_mode=ParseMode.HTML
    )

    print(f"✅ Jour {day} envoyé avec succès : {message['topic']}")

# ─── Point d'entrée ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(post_daily_message())
