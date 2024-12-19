import asyncio
import base64

from telegram import Bot, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


class TelegramClient:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.bot = Bot(self.bot_token)
        self.registered_user = {}
        self.thread = None

    async def command_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Benvenuto! Inviami il tuo codice per registrarti al servizio."
        )

    # Funzione per registrare l'utente
    async def register_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_user.id
        wadas_user_id = update.message.text

        # Salvataggio del codice associato all'utente
        self.registered_user[wadas_user_id] = chat_id
        print(chat_id)
        await update.message.reply_text("Registrazione completata!")

    async def send_notification(self, wadas_user_id: str, message: str, image_b64=None) -> None:
        if image_b64:
            image_data = base64.b64decode(image_b64)
            await self.bot.send_photo(
                chat_id=self.registered_user[wadas_user_id], photo=image_data, caption=message
            )
        else:
            await self.bot.send_message(chat_id=self.registered_user[wadas_user_id], text=message)

    async def send_notifications(self, user_ids: list[str], message: str, image_b64=None) -> None:
        """
        Invia notifiche a una lista di utenti in parallelo.
        """
        tasks = [self.send_notification(user_id, message, image_b64) for user_id in user_ids]
        await asyncio.gather(*tasks, return_exceptions=True)

    def is_user_registered(self, wadas_user_id):
        if (
            wadas_user_id in self.registered_user
            and self.registered_user[wadas_user_id] is not None
        ):
            return True
        return False

    def start(self):
        application = (
            Application.builder().token(self.bot_token).read_timeout(30).write_timeout(30).build()
        )

        application.add_handler(CommandHandler("start", self.command_start))

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.register_user))

        # Avvio del bot
        application.run_polling()
