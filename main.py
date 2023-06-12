import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackContext, CommandHandler,
                          MessageHandler, filters)

from exceptions import *
from my_logger import InterceptHandler
from weather import form_weather

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=("Привет! Я могу показать погоду в каком-то месте.\n"
                "Чтобы начать просто отправь геопозицию любого места.")
    )


async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Упс. Я не знаю такую команду"
    )


async def location(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if update.edited_message:
        return
        message = update.edited_message
    else:
        message = update.message
    
    try:
        response = form_weather(message.location)
    except:
        response = "Не удалось определить погоду"
        raise
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=response)


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    if not TOKEN:
        raise TokenNotFound
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Commands handlers
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Location handlers
    location_handler = MessageHandler(filters.LOCATION, location)
    application.add_handler(location_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()