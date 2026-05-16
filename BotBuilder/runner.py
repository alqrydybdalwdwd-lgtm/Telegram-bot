import telebot
from telebot import types
import json
import threading

DB_FILE = "db.json"


def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


db = load_db()


def run_bot(bot_name, data):

    token = data["token"]
    owner = data["owner"]

    bot = telebot.TeleBot(token)

    waiting_text = {}

    print(f"BOT STARTED => {bot_name}")

    @bot.message_handler(commands=['start'])
    def start(message):

        if str(message.chat.id) == owner:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            markup.add("➕ إضافة رد")
            markup.add("📂 الردود")
            markup.add("❌ حذف رد")

            bot.send_message(
                message.chat.id,
                f"مرحباً بك في لوحة تحكم بوتك 🔥\n\nاسم البوت:\n{bot_name}",
                reply_markup=markup
            )

        else:
            bot.send_message(
                message.chat.id,
                "أهلاً بك 👋"
            )

    @bot.message_handler(func=lambda m: m.text == "➕ إضافة رد")
    def add_reply(message):

        if str(message.chat.id) != owner:
            return

        msg = bot.send_message(
            message.chat.id,
            "أرسل الكلمة الآن:"
        )

        bot.register_next_step_handler(
            msg,
            get_keyword
        )

    def get_keyword(message):

        waiting_text[message.chat.id] = message.text

        msg = bot.send_message(
            message.chat.id,
            "أرسل الرد الآن (نص أو صورة أو ملف):"
        )

        bot.register_next_step_handler(
            msg,
            save_reply
        )

    def save_reply(message):

        keyword = waiting_text.get(message.chat.id)

        if not keyword:
            return

        if "replies" not in data:
            data["replies"] = {}

        if message.content_type == "text":

            data["replies"][keyword] = {
                "type": "text",
                "content": message.text
            }

        elif message.content_type == "photo":

            file_id = message.photo[-1].file_id

            data["replies"][keyword] = {
                "type": "photo",
                "content": file_id
            }

        elif message.content_type == "document":

            file_id = message.document.file_id

            data["replies"][keyword] = {
                "type": "document",
                "content": file_id
            }

        db = load_db()

        for uid in db:
            if bot_name in db[uid]["bots"]:
                db[uid]["bots"][bot_name] = data

        save_db(db)

        bot.send_message(
            message.chat.id,
            "تم حفظ الرد بنجاح 🔥"
        )

    @bot.message_handler(func=lambda m: True)
    def all_messages(message):

        text = message.text

        replies = data.get("replies", {})

        if text in replies:

            reply_data = replies[text]

            if reply_data["type"] == "text":

                bot.reply_to(
                    message,
                    reply_data["content"]
                )

            elif reply_data["type"] == "photo":

                bot.send_photo(
                    message.chat.id,
                    reply_data["content"]
                )

            elif reply_data["type"] == "document":

                bot.send_document(
                    message.chat.id,
                    reply_data["content"]
                )

    bot.infinity_polling()


for uid in db:

    bots = db[uid]["bots"]

    for bot_name in bots:

        data = bots[bot_name]

        thread = threading.Thread(
            target=run_bot,
            args=(bot_name, data)
        )

        thread.start()
