from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.commands import start_command, help_command, test_command
from handlers.conversations import conv_handler
from handlers.messages import echo

def main():
    TOKEN = '7416118678:AAESC9LJr4ofyBl9oKOdUxsXV7mJXMQynbA'
    application = Application.builder().token(TOKEN).build()

# для коммита
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('test', test_command))

    # Регистрация обработчиков диалогов
    application.add_handler(conv_handler)

    # Регистрация обработчиков сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
