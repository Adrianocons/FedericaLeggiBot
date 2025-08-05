

import logging
import os
import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
FEDE_USER_ID = os.environ.get("FEDE_USER_ID") 

if not BOT_TOKEN:
    raise RuntimeError("La variabile d’ambiente BOT_TOKEN non è impostata")

if not FEDE_USER_ID:
    raise RuntimeError("La variabile d’ambiente FEDE_USER_ID non è impostata")

PATTERN = re.compile(r"\b(?:Fede|Federica)\b", flags=re.IGNORECASE)


async def alert_fede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    text = f"<a href='tg://user?id={FEDE_USER_ID}'>Federica</a> leggi "
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(PATTERN), alert_fede))
    logging.info("Bot avviato. In ascolto dei messaggi…")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

