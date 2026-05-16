import requests
import time

TOKEN = "8952440627:AAExw9NFu194A9BTU1Zyz2vsEMI1H8UeuwM"
URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None):
    url = URL + "/getUpdates"
    if offset:
        url += f"?offset={offset}"
    return requests.get(url).json()

def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        data["reply_markup"] = reply_markup

    requests.post(URL + "/sendMessage", data=data)

def main_menu():
    return {
        "keyboard": [
            ["الموافقة على الانضمام"],
            ["صانع البوتات", "تحويل الصور الى انمي"],
            ["إدارة حساب", "لعبة إكس أو"],
            ["اهداء الاغاني", "بوت الرسائل الصوتية"],
            ["حذف الخلفية من الصور", "المتجر"],
            ["لعبة الروليت", "استخراج روابط القنوات"],
            ["تحويل صيغ الملفات", "معاني اسماء"],
            ["نسخ النصوص", "من زار ملفي الشخصي"],
            ["بوت الأزرار", "تحليل الصور"],
            ["بوت الهمسة", "التعليقات"],
            ["ادارة منشورات القناة", "روبوت المسابقات"],
            ["تحقق من العضو", "سمسمي"],
            ["الاعلانات", "إنشاء منشورات احترافية"]
        ],
        "resize_keyboard": True
    }

def main():
    print("Bot Menu Running...")

    offset = None

    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")

                    if text == "/start":
                        send_message(
                            chat_id,
                            "👋 اختر من القائمة :",
                            reply_markup=main_menu()
                        )

                    elif text == "صانع البوتات":
                        send_message(chat_id, "🚀 قريباً سيتم تفعيل صانع البوتات")

                    elif text == "تحويل الصور الى انمي":
                        send_message(chat_id, "🎨 خدمة تحويل الصور قريباً")

                    elif text == "إدارة حساب":
                        send_message(chat_id, "⚙️ إعدادات الحساب")

                    else:
                        send_message(chat_id, "اختر من القائمة 👇", reply_markup=main_menu())

        time.sleep(1)

if __name__ == "__main__":
    main()
