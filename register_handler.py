from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ReplyKeyboardMarkup

NAME, PHONE, CONFIRM = range(3)


def register(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Nei prossimi passaggi puoi inserire le tue informazioni personali per essere contattato\nUsa /annulla per uscire dalla procedura'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Inserisci il tuo nome e cognome'
    )
    return NAME


def name(update, context):
    name = update.message.text
    id = update.message.from_user['id']
    username = update.message.from_user['username']

    context.chat_data['username'] = username
    context.chat_data['name'] = name

    if('books' not in context.user_data):
        context.user_data['books'] = []

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Insersici il tuo numero di telefono'
    )
    return PHONE


confirm_keyboard_markup = ReplyKeyboardMarkup(
    [['Conferma ✅'], ['Annulla ❌']], one_time_keyboard=True)


def phone(update, context):
    phone = update.message.text
    id = update.message.from_user['id']

    context.chat_data['phone'] = phone

    update.message.reply_text('Ecco un riepilogo dei tuoi dati:\n*Nome: *{name}\n*Cellulare: *{phone}\n*username: *{username}'.format(
        name=context.chat_data['name'],
        phone=context.chat_data['phone'],
        username=context.chat_data['username'],
    ), parse_mode='markdown')
    update.message.reply_text(
        'Confermi?', reply_markup=confirm_keyboard_markup)

    return CONFIRM


def confirm(update, context):
    confirm = update.message.text
    if (confirm == 'Conferma ✅'):
        context.user_data['name'] = context.chat_data['name']
        context.user_data['phone'] = context.chat_data['phone']
        context.user_data['username'] = context.chat_data['username']

        update.message.reply_text(
            'Infromazioni salvate ✅\nOra puoi inserire i tuoi libri da vendere con /vendi')
    else:
        update.message.reply_text('Operazione annullata')
    return ConversationHandler.END


def cancel(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Operazione annullata'
    )
    return ConversationHandler.END


def uknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Comando sconosciuto, riprova o usa /annulla per uscire'
    )
    return None


register_entries = [CommandHandler('registra', register)]
register_states = {
    NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
    PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
    CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm)]
}
register_fallbacks = [CommandHandler(
    'annulla', cancel), MessageHandler(Filters.command, uknown)]

register_handler = ConversationHandler(
    entry_points=register_entries,
    states=register_states,
    fallbacks=register_fallbacks
)
