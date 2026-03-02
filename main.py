import requests
from bs4 import BeautifulSoup
import os
import asyncio
from telegram import Bot
import re

SEARCH_URL = "https://tehnoskarb.ua/ru/mobilnye-telefony-i-smartfony/c1/filter/vendor%3D294"
KEYWORDS = ["iphone air", "iphone 16"]
CHECK_INTERVAL = 600

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Сохраняем товары: {url: price}
products = {}

def extract_price(text):
    match = re.search(r"\d[\d\s]*", text)
    if match:
        return int(match.group().replace(" ", ""))
    return None

async def check_site(bot):
    global products

    r = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.find_all("a", href=True)

    for card in cards:
        title = card.get_text(strip=True).lower()

        if any(keyword in title for keyword in KEYWORDS):
            url = "https://tehnoskarb.ua" + card["href"]

            parent = card.parent.get_text(" ", strip=True)
            price = extract_price(parent)

            if not price:
                continue

            if url not in products:
                products[url] = price
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🔥 Новый товар!\n\n{title}\n💰 {price} грн\n{url}"
                )
            else:
                old_price = products[url]
                if price < old_price:
                    products[url] = price
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=f"📉 Цена снижена!\n\n{title}\nБыло: {old_price} грн\nСтало: {price} грн\n{url}"
                    )

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Бот запущен с отслеживанием цены"
    )

    while True:
        try:
            await check_site(bot)
        except Exception as e:
            print("Ошибка:", e)

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
