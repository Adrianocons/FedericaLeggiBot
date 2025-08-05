import logging
import os
import re

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
FEDE_USERNAME = os.environ.get("FEDE_USERNAME")  

if not BOT_TOKEN or not FEDE_USERNAME:
    raise RuntimeError("Manca BOT_TOKEN o FEDE_USERNAME")

PATTERN = re.compile(r"\b(?:Fede|Federica)\b", flags=re.IGNORECASE)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["enabled"] = True
    await update.message.reply_text("Bot **attivato**! Risponderò quando scrivete Fede o Federica.")

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["enabled"] = False
    await update.message.reply_text("Bot **disattivato**! Non risponderò più.")

async def alert_fede(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.chat_data.get("enabled", True):
        return
    chat_id = update.effective_chat.id
    text = f"Leggi {FEDE_USERNAME}"
    await context.bot.send_message(chat_id=chat_id, text=text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(PATTERN), alert_fede))

    logging.info("Bot avviato. In ascolto dei comandi…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
