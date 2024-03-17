import environ
import requests

from root.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env()

TOKEN = env("TOKEN")
CHAT_ID = env("CHAT_ID")

api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message_to_channel(message, images=None):
    tags = message.get('tags', [])
    subcategories = message.get("subcategories", [])
    film_id = message['film_id']
    subcategory_names = [str(subcategory) for subcategory in subcategories]
    tag_names = [str(tag) for tag in tags]

    formatted_message = (
        f"*Новый запрос*\n"
        f"📌 *Заголовок*: {message['title']}\n"
        f"📝 *Описание*: {message['description']}\n"
        f"📅 *Категория*: {message['category']}\n"
        f"🏷️ *Субкатегория*: {', '.join(subcategory_names)}\n"
        f"🏷️ *Теги*: {', '.join(tag_names)}\n"
        f"🌐 *Страна*: {message['country']}\n"
        f"🌆 *Город*: {message['city']}\n"
        f"📞 *Телефон*: {message['telephone']}\n"
        f"📞 *Телеграм*: {message['telegram']}\n"
        f"📋 *Тип*: {message['тип']}\n"
    )

    if message['is_price_negotiable']:
        formatted_message += "💰 *Цена*: Договорная\n"
    else:
        formatted_message += f"💰 *Цена*: {message['price']}\n"

    inline_kb = {
        "inline_keyboard": [
            [{"text": "👍", "callback_data": f"button1_{film_id}"}, {"text": "👎", "callback_data": f"button2_{film_id}"}]
        ]
    }

    payload = {
        "chat_id": CHAT_ID,
        "text": formatted_message,
        "parse_mode": "markdown",
        "reply_markup": inline_kb
    }

    if images:
        files = {('photo', open(f"{BASE_DIR}/{image_path}", 'rb')) for image_path in images}
        response = requests.post(api_url, files=files)
    else:
        response = requests.post(api_url, json=payload)

    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    else:
        print("Message sent successfully!")
