from os import getenv
from dotenv import load_dotenv
import logging
from telegram import Update, helpers, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters
import calculate as calc
from pics_generator import Calendar
from db_manage import DataBase

load_dotenv()
TOKEN = getenv("TOKEN")
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")
db = DataBase("TgCalendar", USER, HOST, DB_PASSWORD)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

with open("manual") as f:
    manual = f.read()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = helpers.create_deep_linked_url(context.bot.username, "gid_" + str(update.effective_chat.id))
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="Push me!", url=url)
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=manual, reply_markup=keyboard)


async def create_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    event_name = "test_name"
    date1 = "08.07.2023"
    date2 = "10.07.2023"
    event_id = calc.get_event_id(context.args[0][4:], event_name, date1, date2)
    picture_path = "pictures/" + str(event_id) + ".png"
    url = helpers.create_deep_linked_url(context.bot.username, "eid_" + str(event_id))
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="FINISH", url=url)
    )
    text = "Just Do IT"
    await db.create("calendars", {"group_id": context.args[0][4:], "event_id": event_id, "event_name": event_name,
                    "active": True, "picture_path": picture_path})
    await generate_picture(update, context, date1, date2, picture_path)
    await context.bot.send_message(update.effective_chat.id, text, reply_markup=keyboard)


async def generate_picture(update: Update, context: ContextTypes.DEFAULT_TYPE, date1, date2, path):
    calendar = Calendar(date1, date2, " ".join(context.args[1:]))
    calendar.save(path)
    pic_message = (await context.bot.send_photo(chat_id=update.effective_chat.id, photo=path))
    await context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=pic_message.message_id)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start", create_calendar, filters.Regex("gid_")))

    application.run_polling()
