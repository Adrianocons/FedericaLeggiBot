import logging
import os
import re
import json
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
FEDE_USERNAME = os.environ.get("FEDE_USERNAME")

if not BOT_TOKEN or not FEDE_USERNAME:
    raise RuntimeError("BOT_TOKEN o FEDE_USERNAME non impostati nelle variabili d'ambiente")

FEDE_USERNAME_CLEAN = FEDE_USERNAME.lstrip("@").lower()

KEYWORDS = [
    r"\bFede",
    r"\bFederica\b",
    r"porco\s*dio",
    r"dio\s*cane",
    r"\bMussolini\b",
    r"\dux\b",
]

PATTERN = re.compile("|".join(KEYWORDS), flags=re.IGNORECASE)

COMMANDS_FILE = "commands.json"

if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        CUSTOM_COMMANDS = json.load(f)
else:
    CUSTOM_COMMANDS = {
        "!notizia": "Ho letto la notizia di un gatto morto per colpa di una streamer, il gatto si chiamava Sebastiano per i amici Sebi",
    }

def save_commands():
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(CUSTOM_COMMANDS, f, ensure_ascii=False, indent=2)

START_TIME = datetime.now(timezone.utc)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username and update.effective_user.username.lower() == FEDE_USERNAME_CLEAN:
        return
    context.chat_data["enabled"] = True
    await update.message.reply_text("Bot attivato!")

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username and update.effective_user.username.lower() == FEDE_USERNAME_CLEAN:
        return
    context.chat_data["enabled"] = False
    await update.message.reply_text("Bot disattivato!")

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username and update.effective_user.username.lower() == FEDE_USERNAME_CLEAN:
        return
    if update.message.date < START_TIME:
        return
    try:
        text = update.message.text.replace("/addcomando", "", 1).strip()
        name, response = map(str.strip, text.split(",", 1))
        if not name.startswith("!"):
            name = f"!{name}"
        CUSTOM_COMMANDS[name.lower()] = response
        save_commands()
        await update.message.reply_text(f"Comando {name} aggiunto con successo.")
    except Exception:
        await update.message.reply_text("Errore nel formato. Usa: /addcomando nomecomando,testodelcomando")

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username and update.effective_user.username.lower() == FEDE_USERNAME_CLEAN:
        return
    if update.message.date < START_TIME:
        return
    try:
        name = update.message.text.replace("/removecomando", "", 1).strip()
        if not name.startswith("!"):
            name = f"!{name}"
        if name.lower() in CUSTOM_COMMANDS:
            del CUSTOM_COMMANDS[name.lower()]
            save_commands()
            await update.message.reply_text(f"Comando {name} rimosso.")
        else:
            await update.message.reply_text(f"Comando {name} non trovato.")
    except Exception:
        await update.message.reply_text("Errore. Usa: /removecomando nomecomando")

async def alert_fede(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.date < START_TIME:
        return
    if not context.chat_data.get("enabled", True):
        return
    chat_id = update.effective_chat.id
    text = f"Leggi {FEDE_USERNAME}"
    await context.bot.send_message(chat_id=chat_id, text=text)

async def handle_custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.date < START_TIME:
        return
    message = update.message.text.strip()
    command = message.split()[0].lower()
    if command in CUSTOM_COMMANDS:
        await update.message.reply_text(CUSTOM_COMMANDS[command])

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("stop", stop_cmd))
    application.add_handler(CommandHandler("addcomando", add_command))
    application.add_handler(CommandHandler("removecomando", remove_command))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(PATTERN), alert_fede))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^!"), handle_custom_command))

    logging.info("Bot avviato. In ascolto dei messaggi e comandi…")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
