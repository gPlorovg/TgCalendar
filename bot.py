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
    group_id = int(context.args[0][4:])
    event_id = calc.get_event_id(str(group_id), event_name, date1, date2)
    picture_path = "pictures/" + str(event_id) + ".png"
    url = helpers.create_deep_linked_url(context.bot.username, "eid_" + str(event_id))
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="FINISH", url=url)
    )
    text = "Just Do IT"
    db.create("calendars", {"group_id": group_id, "event_id": event_id, "event_name": event_name,
              "active": True, "picture_path": picture_path})
    db.commit()
    calendar = Calendar(date1, date2, event_name)
    calendar.save(picture_path)
    pic_message = await context.bot.send_photo(chat_id=group_id, photo=picture_path)
    await context.bot.pin_chat_message(chat_id=group_id, message_id=pic_message.message_id)
    await context.bot.send_message(chat_id=group_id, text=text, reply_markup=keyboard)


async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Vote")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    # Make sure the deep-linking handlers occur *before* the normal /start handler.
    application.add_handler(CommandHandler("start", create_calendar, filters.Regex("gid_")))
    application.add_handler(CommandHandler("start", vote, filters.Regex("eid_")))
    application.add_handler(CommandHandler("start", start))

    application.run_polling()
