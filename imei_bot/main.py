import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    Dispatcher

from imei_bot.handlers import start_handler, message_handler

load_dotenv()


def setup_handlers(dispatcher: Dispatcher) -> None:
    """Установка всех обработчиков"""
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))


def main() -> None:
    """Основная функция для запуска бота"""
    updater: Updater = Updater(os.getenv('BOT_TOKEN'), use_context=True)
    dispatcher: Dispatcher = updater.dispatcher
    setup_handlers(dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
