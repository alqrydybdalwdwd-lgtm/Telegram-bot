import telebot
import json
import threading

DB_FILE = "db.json"


def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def run_bot(token, rules):

    try:
        bot = telebot.TeleBot(token)

        @bot.message_handler(func=lambda m: True)
        def all_messages(message):

            text = message.text

            if text in rules:
                bot.reply_to(message, rules[text])

        print(f"Bot started: {token}")

        bot.infinity_polling()

    except Exception as e:
        print("ERROR:", e)


db = load_db()

for uid in db:

    user_bots = db[uid]["bots"]

    for bot_name in user_bots:

        data = user_bots[bot_name]

        token = data.get("token")
        rules = data.get("rules", {})

        if token:

            thread = threading.Thread(
                target=run_bot,
                args=(token, rules)
            )

            thread.start()
