import requests
from bs4 import BeautifulSoup
import time
import os
from telegram import Bot

SEARCH_URL = "https://tehnoskarb.ua/ru/mobilnye-telefony-i-smartfony/c1/filter/vendor%3D294"
KEYWORDS = ["iphone air", "iphone 16", "iphone 16 pro", "iphone 17"]
CHECK_INTERVAL = 600

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)
bot.send_message(chat_id=CHAT_ID, text="✅ Бот запущен и работает")
headers = {
    "User-Agent": "Mozilla/5.0"
}

found = []

def check_site():
    r = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    products = []

    for item in soup.find_all("a", href=True):
        title = item.get_text(strip=True).lower()

        if any(keyword in title for keyword in KEYWORDS):
            url = "https://tehnoskarb.ua" + item["href"]
            products.append((title, url))

    return products

while True:
    try:
        items = check_site()

        for item in items:
            if item not in found:
                found.append(item)
                bot.send_message(chat_id=CHAT_ID, text=f"🔥 Новый товар!\n\n{item[0]}\n{item[1]}")

    except Exception as e:
        print("Ошибка:", e)

    time.sleep(CHECK_INTERVAL)
