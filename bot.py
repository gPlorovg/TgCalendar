from os import getenv
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import calculate as calc
from pics_generator import Calendar

load_dotenv()
TOKEN = getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="To create calendar text /create command"
                                                                          " with edge dates of your event and it's name"
                                                                          "\nLike this: /create 08.07-10.07"
                                                                          " Author birthday party")


async def create_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    year = calc.get_year()
    date1 = context.args[0].split("-")[0] + "." + str(year)
    date2 = context.args[0].split("-")[1] + "." + str(year)
    calendar = Calendar(date1, date2, " ".join(context.args[1:]))
    path = "calendar for" + " ".join(context.args[1:]) + ".png"
    calendar.save(path)
    pic_message = (await context.bot.send_photo(chat_id=update.effective_chat.id, photo=path))
    await context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=pic_message.message_id)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    create_handler = CommandHandler("create", create_calendar)
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(create_handler)

    application.run_polling()
