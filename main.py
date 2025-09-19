import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

# إعدادات تلغرام
TELEGRAM_TOKEN = os.environ.get('8289814129:AAGhJL_DjLl104OwK1RsxZ90DiNP6hynqGc')
CHAT_ID = os.environ.get('198842533')

def send_telegram_message(message):
    """إرسال رسالة على تلغرام"""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
        print("تم إرسال الرسالة إلى تلغرام")
    except Exception as e:
        print(f"خطأ في إرسال الرسالة: {e}")

def search_jobs():
    """بحث بسيط عن وظائف"""
    try:
        message = "✅ تم تشغيل برنامج البحث عن الوظائف بنجاح!\nالبرنامج يعمل كل 3 ساعات."
        send_telegram_message(message)
        print("تم التشغيل بنجاح")
    except Exception as e:
        print(f"خطأ في البرنامج: {e}")

def main():
    """الدالة الرئيسية"""
    print("جاري تشغيل برنامج البحث عن الوظائف...")
    search_jobs()

if __name__ == "__main__":
    main()
