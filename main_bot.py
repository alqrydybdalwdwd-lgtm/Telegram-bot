import telebot
import json
from telebot import types
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
        json.dump(data, f, indent=2)

db = load_db()


@bot.message_handler(commands=['start'])
def start(message):

    uid = str(message.chat.id)

    if uid not in db:
        db[uid] = {"bots": {}}
        save_db(db)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("قائمة بوتاتك")
    btn2 = types.KeyboardButton("إنشاء بوت جديد")

    markup.add(btn1)
    markup.add(btn2)

    bot.send_message(
        message.chat.id,
        f"""أهلاً بك ( {message.from_user.first_name} ) في بوت صنع بوتات

- يمكنك صنع أي بوت تريده مجانا""",
        reply_markup=markup
    )


@bot.message_handler(commands=['mybots'])
def mybots(message):
    uid = str(message.chat.id)
    bots = db.get(uid, {}).get("bots", {})

    if not bots:
        bot.send_message(message.chat.id, "لا يوجد بوتات حالياً.")
        return

    text = "بوتاتك:\n"
    for b in bots:
        text += f"- {b}\n"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['newbot'])
def newbot(message):
    msg = bot.send_message(message.chat.id, "اكتب اسم البوت:")
    bot.register_next_step_handler(msg, save_bot_name)


def save_bot_name(message):
    uid = str(message.chat.id)
    name = message.text

    db[uid]["bots"][name] = {
        "token": "",
        "rules": {}
    }

    save_db(db)

    msg = bot.send_message(message.chat.id, "أرسل توكن البوت الآن:")
    bot.register_next_step_handler(msg, save_token, uid, name)


def save_token(message, uid, name):
    token = message.text

    db[uid]["bots"][name]["token"] = token
    save_db(db)

    bot.send_message(message.chat.id, "تم إنشاء البوت بنجاح 🔥")


@bot.message_handler(commands=['add'])
def add_rule(message):
    msg = bot.send_message(
        message.chat.id,
        "اكتب بهذا الشكل:\nاسم البوت | الكلمة | الرد"
    )
    bot.register_next_step_handler(msg, save_rule)


def save_rule(message):
    uid = str(message.chat.id)

    try:
        bot_name, key, reply = message.text.split("|")

        bot_name = bot_name.strip()
        key = key.strip()
        reply = reply.strip()

        db[uid]["bots"][bot_name]["rules"][key] = reply
        save_db(db)

        bot.send_message(message.chat.id, "تم إضافة الرد بنجاح ✔️")

    except:
        bot.send_message(message.chat.id, "خطأ في الصيغة!")
@bot.message_handler(func=lambda message: message.text == "إنشاء بوت جديد")
def create_new_bot(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("بوت الردود")
    markup.add("بوت الأزرار")
    markup.add("بوت الهمسة")
    markup.add("بوت الترجمة")
    markup.add("تحويل الصور الى انمي")
    markup.add("لعبة اكس او")
    markup.add("رجوع")

    bot.send_message(
        message.chat.id,
        "اختر من القائمة :",
        reply_markup=markup
    )
@bot.message_handler(func=lambda message: message.text == "بوت الردود")
def reply_bot_selected(message):

    msg = bot.send_message(
        message.chat.id,
        "ارسل اسم بوت الردود:"
    )

    bot.register_next_step_handler(msg, save_bot_name)

bot.polling()
