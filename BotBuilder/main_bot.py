import telebot
from telebot import types
import json

TOKEN = "8932837313:AAFOuz_ahQ3TOkJ_wSxEy_UXOqJzCJlxufg"

bot = telebot.TeleBot(TOKEN)

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


@bot.message_handler(commands=['start'])
def start(message):

    uid = str(message.chat.id)

    if uid not in db:
        db[uid] = {
            "bots": {}
        }
        save_db(db)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("➕ إنشاء بوت جديد")
    btn2 = types.KeyboardButton("📂 قائمة بوتاتك")

    markup.add(btn1)
    markup.add(btn2)

    bot.send_message(
        message.chat.id,
        f"""
أهلاً بك {message.from_user.first_name}

في بوت صناعة البوتات الاحترافي 🔥

يمكنك إنشاء بوتات متعددة بسهولة.
""",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "➕ إنشاء بوت جديد")
def create_bot(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🤖 بوت الردود")
    markup.add("🔘 بوت الأزرار")
    markup.add("🎵 بوت الأغاني")
    markup.add("🖼 بوت الصور")
    markup.add("🔙 رجوع")

    bot.send_message(
        message.chat.id,
        "اختر نوع البوت:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "🤖 بوت الردود")
def reply_bot(message):

    msg = bot.send_message(
        message.chat.id,
        "أرسل اسم البوت:"
    )

    bot.register_next_step_handler(msg, save_bot_name)


def save_bot_name(message):

    uid = str(message.chat.id)

    bot_name = message.text.strip()

    msg = bot.send_message(
        message.chat.id,
        "أرسل توكن البوت الآن:"
    )

    bot.register_next_step_handler(
        msg,
        save_bot_token,
        uid,
        bot_name
    )


def save_bot_token(message, uid, bot_name):

    token = message.text.strip()

    if uid not in db:
        db[uid] = {
            "bots": {}
        }

    db[uid]["bots"][bot_name] = {
        "token": token,
        "type": "reply",
        "owner": uid,
        "replies": {}
    }

    save_db(db)

    bot.send_message(
        message.chat.id,
        f"""
تم إنشاء البوت بنجاح 🔥

اسم البوت:
{bot_name}

الآن قم بتشغيل runner.py
"""
    )


@bot.message_handler(func=lambda m: m.text == "📂 قائمة بوتاتك")
def my_bots(message):

    uid = str(message.chat.id)

    if uid not in db:
        bot.send_message(message.chat.id, "لا يوجد بوتات.")
        return

    bots = db[uid]["bots"]

    if not bots:
        bot.send_message(message.chat.id, "لا يوجد بوتات حالياً.")
        return

    text = "📂 بوتاتك:\n\n"

    for bot_name in bots:
        text += f"• {bot_name}\n"

    bot.send_message(message.chat.id, text)


print("MAIN BOT STARTED")

bot.infinity_polling()
