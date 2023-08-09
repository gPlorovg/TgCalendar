from os import getenv
from dotenv import load_dotenv
import logging
from telegram import Update, helpers, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
import json
import calculate as calc
from pics_generator import Calendar
from db_manage import DataBase

load_dotenv()
TOKEN = getenv("TOKEN")
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")
WEB_APP_HOST = getenv("WEB_APP_HOST")
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


async def open_web_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["current_group_id"] = int(context.args[0][4:])
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="WEBAPP", web_app=WebAppInfo(url=WEB_APP_HOST + "/config_calendar"))
    )
    await update.message.reply_text(
        text="Go to web app",
        reply_markup=keyboard
    )


async def web_app_data_manage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app_data = json.loads(update.effective_message.web_app_data.data)
    match web_app_data["action"]:
        case "config":
            await create_calendar(update, context, web_app_data)
        case "vote":
            await get_vote_data(update, context, web_app_data)


async def create_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE, web_app_data: dict):
    # event_name = "test"
    # date1 = "08.07.2023"
    # date2 = "10.07.2023"
    group_id = context.user_data["current_group_id"]
    web_app_data = json.loads(update.effective_message.web_app_data.data)
    event_name = web_app_data["event_name"]
    dates = web_app_data["dates"]
    # date1 = web_app_data["date1"]
    # date2 = web_app_data["date2"]

    event_id = calc.get_event_id(str(group_id), event_name, dates[0])
    picture_path = "pictures/" + str(event_id) + ".png"

    db.create("calendars", {"group_id": group_id, "event_id": event_id, "event_name": event_name,
              "active": True, "picture_path": picture_path})
    db.commit()

    calendar = Calendar(dates, event_name)
    calendar.save(picture_path)

    url = helpers.create_deep_linked_url(context.bot.username, "eid_" + str(event_id))

    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="SEND", callback_data=f"send_calendar_to_group:{group_id}:{picture_path}:{url}")
    )
    await update.message.reply_text(
        text="Finish creation",
        reply_markup=keyboard
    )


async def send_calendar_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _, group_id, picture_path, url = update.callback_query.data.split(":")
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="Vote", url=url)
    )
    text = "Just Do IT"
    pic_message = await context.bot.send_photo(chat_id=group_id, photo=picture_path)
    await context.bot.pin_chat_message(chat_id=group_id, message_id=pic_message.message_id)
    await context.bot.send_message(chat_id=group_id, text=text, reply_markup=keyboard)


async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["current_event_id"] = int(context.args[0][4:])
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="WEBAPP", web_app=WebAppInfo(url=WEB_APP_HOST + "/vote"))
    )
    await update.message.reply_text(
        text="Go to web app",
        reply_markup=keyboard
    )


async def check_user(event_id, chat_id):
    # После нажатия кнопки VOTE
    # Проверка на существования записи по ключу event_id + chat_id в таблице dates
    pass


async def get_vote_data(update: Update, context: ContextTypes.DEFAULT_TYPE, web_app_data: dict):

    event_id = context.user_data["current_event_id"]
    chat_id = update.effective_chat.id
    dates = web_app_data["dates"]
    if await check_user(event_id, chat_id):
        db.update("dates", {"dates": dates})
    else:
        db.create("dates", {"event_id": event_id, "chat_id": chat_id, "dates": dates})

    # Генерация новой картинки
    # Изменение картинки в группе

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    # Make sure the deep-linking handlers occur *before* the normal /start handler.
    application.add_handler(CommandHandler("start", open_web_app, filters.Regex("gid_")))
    application.add_handler(CommandHandler("start", vote, filters.Regex("eid_")))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data_manage))
    application.add_handler(CallbackQueryHandler(send_calendar_to_group, r"send_calendar_to_group"))
    application.add_handler(CommandHandler("start", start))

    application.run_polling()
