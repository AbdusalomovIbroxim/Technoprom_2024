import logging

from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from root.settings import TOKEN, chat_id

logging.basicConfig(level=logging.INFO)

bot_token = TOKEN
chat_id = chat_id
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


async def send_message_to_channel(message, image=None):
    tags = message.get('tags', [])
    film_id = message['film_id']
    # Extract tag names as strings
    tag_names = [str(tag) for tag in tags]

    # Initialize the message text with common fields
    formatted_message = (
        f"*Новый запрос*\n"
        f"📌 *Заголовок*: {message['title']}\n"
        f"📝 *Описание*: {message['description']}\n"
        f"📅 *Категория*: {message['category']}\n"
        f"🏷️ *Субкатегория*: {message['sub_category']}\n"
        f"🏷️ *Теги*: {', '.join(tag_names)}\n"
        f"🌐 *Страна*: {message['country']}\n"
        f"🌆 *Город*: {message['city']}\n"
        f"📞 *Телефон*: {message['telephone']}\n"
        f"📞 *Телеграм*: {message['telegram']}\n"
        f"📋 *Тип*: {message['тип']}\n"
    )

    # Check if there is a price, if not, include "Договорная"
    if message['is_price_negotiable']:
        formatted_message += "💰 *Цена*: Договорная\n"
    else:
        formatted_message += f"💰 *Цена*: {message['price']}\n"

    inline_btn_1 = InlineKeyboardButton('👍', callback_data=f'button1_{film_id}')
    inline_btn_2 = InlineKeyboardButton('👎', callback_data=f'button2_{film_id}')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)

    if image:
        with open(image, "rb") as image_file:
            await bot.send_photo(chat_id=chat_id, photo=image_file, caption=formatted_message, reply_markup=inline_kb1,
                                 parse_mode="markdown")
    else:
        await bot.send_message(chat_id=chat_id, text=formatted_message, reply_markup=inline_kb1, parse_mode="markdown")
