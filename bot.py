from os import getenv
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


load_dotenv()
TOKEN = getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="To create calendar follow next steps:"
                                                                          "1. Text '/create' command"
                                                                          "2. Text me edge dates of your event."
                                                                          "Like this: 08.07.2023-10.07.2023"
                                                                          "3. Text name of the event")


async def create_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Text me edge dates of your event."
                                                                          "Like this: 08.07.2023-10.07.2023")
    await context.bot.ge
    pic_id = (await context.bot.send_photo(chat_id=update.effective_chat.id, photo="test.png")).message_id
    await context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=pic_id)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    create_handler = CommandHandler("create", create_calendar())
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(create_handler)

    application.run_polling()
