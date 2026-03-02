import requests
from bs4 import BeautifulSoup
import time
import os
import asyncio
from telegram import Bot

SEARCH_URL = "https://tehnoskarb.ua/ru/mobilnye-telefony-i-smartfony/c1/filter/vendor%3D294"
KEYWORDS = ["iphone air", "iphone 16", "iphone 17", "iphone 15 pro"]
CHECK_INTERVAL = 600

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

headers = {
    "User-Agent": "Mozilla/5.0"
}

found = set()

async def check_site(bot):
    global found

    r = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.find_all("a", href=True):
        title = item.get_text(strip=True).lower()

        if any(keyword in title for keyword in KEYWORDS):
            url = "https://tehnoskarb.ua" + item["href"]
            key = (title, url)

            if key not in found:
                found.add(key)
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🔥 Новый товар!\n\n{title}\n{url}"
                )

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Бот запущен и работает"
    )

    while True:
        try:
            await check_site(bot)
        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
