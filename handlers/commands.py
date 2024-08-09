from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import random

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greetings = ["Привет!", "Здравствуйте!", "Добрый день!"]
    greeting = random.choice(greetings)
    keyboard = [[InlineKeyboardButton("Пройти тест", callback_data='start_test')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'{greeting} Пройдите тест!', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Доступные команды:\n/start - начать\n/help - помощь\n/test - тестовая команда')

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Это тестовая команда.')
