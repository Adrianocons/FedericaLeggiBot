
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


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


BOT_TOKEN = os.environ.get("BOT_TOKEN")
FEDE_USERNAME = os.environ.get("FEDE_USERNAME") 

if not BOT_TOKEN:
    raise RuntimeError("La variabile d'ambiente BOT_TOKEN non è impostata")

if not FEDE_USERNAME:
    raise RuntimeError("La variabile d'ambiente FEDE_USERNAME non è impostata")

PATTERN = re.compile(r"\b(?:Fede|Federica)\b", flags=re.IGNORECASE)

FEDE_USERNAME_CLEAN = FEDE_USERNAME.lstrip("@").lower()


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username and update.effective_user.username.lower() == FEDE_USERNAME_CLEAN:
        return
    context.chat_data["enabled"] = True
    await update.message.reply_text("Bot attivato")


async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username and update.effective_user.username.lower() == FEDE_USERNAME_CLEAN:
        return
    context.chat_data["enabled"] = False
    await update.message.reply_text("Bot disattivato")


async def alert_fede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.chat_data.get("enabled", True):
        return
    chat_id = update.effective_chat.id
    text = f"leggi {FEDE_USERNAME}"
    await context.bot.send_message(chat_id=chat_id, text=text)


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("stop", stop_cmd))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(PATTERN), alert_fede))

    logging.info("Bot avviato. In ascolto dei messaggi…")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
