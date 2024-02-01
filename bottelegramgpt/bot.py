#!/usr/bin/env python3


import logging
import requests

from telegram import Update


from telegram.ext import (filters, MessageHandler, ApplicationBuilder,
                          CommandHandler, ContextTypes)

# Ключ API из личного кабинета https://ask.chadgpt.ru/
CHAD_API_KEY = 'enter your API key'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Это мой первый бот, позволяет общаться с GPT через API ask"
    )


async def echo(update: Update, context):
    text = update.message.text

    # Формируем текстовое сообщение в API
    request_json = {
        "message": text,
        "api_key": "chad-cf06795bc14346e88968c82fe41ff1384fb9fdme"
    }

    # Отправляем запрос на адрес в зависимости от желаемой версии GPT
    # Можно установить - https://ask.chadgpt.ru/api/public/gpt-4

    response = requests.post(
        url='https://ask.chadgpt.ru/api/public/gpt-4',
        json=request_json,
        timeout=10  # Set a reasonable timeout value in seconds
    )
    # Проверка сутатуса запроса
    if response.status_code != 200:
        print(f'Error! HTTP response code: {response.status_code}')
    else:
        # Получите responsetext и преобразуйте его в dict
        resp_json = response.json()
        if resp_json['is_success']:
            resp_msg = resp_json['response']
            used_words = resp_json['used_words_count']
            print(f'Response from bot: {resp_msg}\nUsed words: {used_words}')
            # Отправляем ответ API пользователю в telegram
            await update.message.reply_text(resp_msg)
        else:
            error = resp_json['error_message']
            print(f'Error: {error}')


echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)


if __name__ == '__main__':
    # Токен telegram
    application = ApplicationBuilder().token(
        'enter your telegram token').build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)

    application.run_polling()
    application.run()
