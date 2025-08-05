

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

# Logging di base
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Variabili d’ambiente
BOT_TOKEN = os.environ.get("8382220036:AAHQTILQQF0IJ6WCoeYdsamrU5pdQjalnAQ")
FEDE_USER_ID = os.environ.get("FedericaPutti")  # stringa numerica

if not BOT_TOKEN:
    raise RuntimeError("La variabile d’ambiente BOT_TOKEN non è impostata")

if not FEDE_USER_ID:
    raise RuntimeError("La variabile d’ambiente FEDE_USER_ID non è impostata")

# Regex per intercettare “Fede” o “Federica”
PATTERN = re.compile(r"\b(?:Fede|Federica)\b", flags=re.IGNORECASE)


async def alert_fede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Invia il messaggio di menzione a Federica."""
    chat_id = update.effective_chat.id
    text = f"<a href='tg://user?id={FEDE_USER_ID}'>Federica</a> leggi "
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def main() -> None:
    """Avvia il bot in modalità polling."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handler per i messaggi contenenti le parole chiave
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(PATTERN), alert_fede))

    logging.info("Bot avviato. In ascolto dei messaggi…")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
