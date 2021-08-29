from register_handler import register_handler
from start_handler import start_handler
from add_handler import add_handler
from telegram.ext import Updater, PicklePersistence
import config


def main():

    API_KEY = config.API_KEY
    persistence = PicklePersistence('bot_persistance')

    updater = Updater(token=API_KEY, use_context=True, persistence=persistence)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(add_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
