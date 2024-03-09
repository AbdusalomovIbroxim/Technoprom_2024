# import logging
#
# from aiogram import Bot, Dispatcher
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
# from django.contrib.auth import get_user_model
#
# from root.settings import TOKEN, CHAT_ID
# from .models import Message
#
# logging.basicConfig(level=logging.INFO)
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)
# User = get_user_model()
#
#
# async def send_message(user_id, amount, photo):
#     inline_kb = [
#         InlineKeyboardButton(text="Добавить", callback_data=f"+"),
#         InlineKeyboardButton(text="Перейти",
#                              url="https://tecnoprom-2024.onrender.com/users/profile/{}".format(user_id)),
#     ]
#
#     message = f"""
#     User id: {user_id}
#
#     Amount: {amount}
#
#
#     """
#
#     inline_query = InlineKeyboardMarkup(row_width=1).row(*inline_kb)
#     # with open(photo, "rb"):
#     await bot.send_photo(
#         chat_id=CHAT_ID,
#         photo=InputFile(photo.file),
#         reply_markup=inline_query,
#         caption=amount,
#     )
#
#
# async def send_message_to_channel(message_data, pk):
#     message = f"Новая компания зарегистрирована:\n{pk}\n\n"
#     for key, value in message_data.items():
#         if key == "Website" or key == "URL Maps":
#             if value:
#                 message += f"*{key}:* [{key}]({value})\n"
#         else:
#             if value:
#                 message += f"*{key}:* {value}\n"
#
#     # buttons = [
#     inline_kb1 = InlineKeyboardButton(
#         text="Активировать", callback_data=f"activate_company_{pk}"
#     )
#     inline_kb2 = InlineKeyboardButton(
#         text="Деактивировать", callback_data=f"dis_activate_company_{pk}"
#     )
#     # ]
#     inline_kb = InlineKeyboardMarkup().add(inline_kb1, inline_kb2)
#
#     await bot.send_message(
#         chat_id=CHAT_ID, text=message, parse_mode="markdown", reply_markup=inline_kb
#     )
#
#
# def false_account_status(pk: int):
#     account = User.objects.get(pk=pk)
#     account.is_business_account = False
#     account.save()
#     user = Message.objects.create(
#         sender_id=1, message=f"Ваш запрос на бизнес аккаунт был принят"
#     )
#     user.recipients.add(pk)
#     user.save()
#     return "status false"
#
#
# def true_account_status(pk: int):
#     account = User.objects.get(pk=pk)
#     account.is_business_account = True
#     account.save()
#     user = Message.objects.create(
#         sender_id=1, message=f"Ваш запрос на бизнес аккаунт был отклонен"
#     )
#     user.recipients.add(pk)
#     user.save()
#     return "status true"

import requests
from root.settings import TOKEN, CHAT_ID
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


async def send_message(user_id, amount, photo):
    inline_kb = {
        "inline_keyboard": [
            [{"text": "Добавить", "callback_data": "+"}, {"text": "Перейти", "url": f"https://tecnoprom-2024.onrender.com/users/profile/{user_id}"}]
        ]
    }

    message_text = f"User id: {user_id}\nAmount: {amount}\n"
    payload = {
        "chat_id": CHAT_ID,
        "text": message_text,
        "parse_mode": "markdown",
        "reply_markup": inline_kb
    }

    files = {'photo': photo}
    response = requests.post(TELEGRAM_API_URL, data=payload, files=files)

    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    else:
        print("Message sent successfully!")


async def send_message_to_channel(message_data, pk):
    message = "Новая компания зарегистрирована:\n{}\n\n".format(pk)
    for key, value in message_data.items():
        if key == "Website" or key == "URL Maps":
            if value:
                message += "*{}:* [{}]({})\n".format(key, key, value)
        else:
            if value:
                message += "*{}:* {}\n".format(key, value)

    inline_kb = {
        "inline_keyboard": [
            [{"text": "Активировать", "callback_data": "activate_company_{}".format(pk)},
             {"text": "Деактивировать", "callback_data": "dis_activate_company_{}".format(pk)}]
        ]
    }

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "markdown",
        "reply_markup": inline_kb
    }

    response = requests.post(TELEGRAM_API_URL, json=payload)

    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    else:
        print("Message sent successfully!")


def false_account_status(pk: int):
    account = User.objects.get(pk=pk)
    account.is_business_account = False
    account.save()
    user = Message.objects.create(
        sender_id=1, message="Ваш запрос на бизнес аккаунт был принят"
    )
    user.recipients.add(pk)
    user.save()
    return "status false"


def true_account_status(pk: int):
    account = User.objects.get(pk=pk)
    account.is_business_account = True
    account.save()
    user = Message.objects.create(
        sender_id=1, message="Ваш запрос на бизнес аккаунт был отклонен"
    )
    user.recipients.add(pk)
    user.save()
    return "status true"
