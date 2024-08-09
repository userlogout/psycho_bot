from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

TEST, SCORE = range(2)

questions = [
    "Вопрос 1: Вы чувствуете себя подавленным?",
    "Вопрос 2: Вам трудно сосредоточиться?",
    "Вопрос 3: У вас проблемы со сном?"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['score'] = 0
    context.user_data['question_index'] = 0
    keyboard = [
        [InlineKeyboardButton("Да", callback_data='yes'), InlineKeyboardButton("Нет", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(questions[0], reply_markup=reply_markup)
    return TEST

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    answer = query.data
    if answer == 'yes':
        context.user_data['score'] += 1
    context.user_data['question_index'] += 1
    if context.user_data['question_index'] < len(questions):
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='yes'), InlineKeyboardButton("Нет", callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(questions[context.user_data['question_index']], reply_markup=reply_markup)
        return TEST
    else:
        return await show_results(update, context)

async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    score = context.user_data['score']
    if score < 2:
        result_text = "У вас нет депрессии."
        photo_url = "URL_фото_с_котом"
    else:
        result_text = "У вас может быть депрессия."
        photo_url = "URL_фото_с_человеком"

    context.user_data['test_results'] = result_text
    await update.callback_query.message.reply_text(result_text)
    await update.callback_query.message.reply_photo(photo_url)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Тест прерван.')
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start, pattern='start_test')],
    states={
        TEST: [CallbackQueryHandler(test, pattern='^(yes|no)$')],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    per_message=True
)
