from telegram.ext import CommandHandler


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi')


start_handler = CommandHandler('start', start)
