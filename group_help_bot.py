from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

TOKEN = "8952440627:AAGfgd7rL69EiV9Dy4XexXKzhiw3pDNEdtg"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً 👋 أنا بوت ردود تلقائي.\nاكتب أي رسالة وسأرد عليك 🤖"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "الأوامر:\n"
        "/start - تشغيل البوت\n"
        "/help - المساعدة\n"
    )

# الردود التلقائية
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    replies = {
        "السلام": "وعليكم السلام 🌹",
        "مرحبا": "أهلاً وسهلاً 👋",
        "هلا": "هلا فيك 😎",
        "كيف الحال": "تمام الحمدلله 😊",
        "بوت": "نعم 🤖 أنا بوت ردود"
    }

    for k, v in replies.items():
        if k in text:
            await update.message.reply_text(v)
            return


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

app.run_polling()
