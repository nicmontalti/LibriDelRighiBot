from os import stat
from re import sub
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ReplyKeyboardMarkup
from uuid import uuid4
from add_book import add_book

TITLE, AUTHOR, SUBJECT, CLASS, EDITION, CONFIRM = range(6)

subjects = [['Biology (Cambridge)'],
            ['Filosofia'],
            ['Fisica'],
            ['Ginnastica'],
            ['Informatica'],
            ['Inglese'],
            ['Italiano'],
            ['Latino'],
            ['Matematica'],
            ['Mathematics (Cambridge)'],
            ['Physics (Cambridge)'],
            ['Religione'],
            ['Scienze'],
            ['Storia'],
            ['Storia dell\'arte / Disegno']]

classes = [list(range(1, 6))]

subjects_keyboard_markup = ReplyKeyboardMarkup(
    subjects, one_time_keyboard=True)
classes_keyboard_markup = ReplyKeyboardMarkup(classes, one_time_keyboard=True)
confirm_keyboard_markup = ReplyKeyboardMarkup(
    [['Conferma ✅'], ['Annulla ❌']], one_time_keyboard=True)


def add(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Qui puoi inserire un libro da vendere, segui le istruzioni'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Titolo'
    )
    return TITLE


def title(update, context):
    if (context.user_data['name'] is None):
        raise Exception

    book_id = str(uuid4())
    title = update.message.text

    context.chat_data['book_id'] = book_id
    context.chat_data['title'] = title

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Autore')

    return AUTHOR


def author(update, context):
    author = update.message.text
    context.chat_data['author'] = author

    update.message.reply_text('Seleziona la materia:',
                              reply_markup=subjects_keyboard_markup)

    return SUBJECT


def subject(update, context):
    subject = update.message.text
    context.chat_data['subject'] = subject

    update.message.reply_text('Seleziona la classe:',
                              reply_markup=classes_keyboard_markup)

    return CLASS


def klass(update, context):
    klass = update.message.text
    context.chat_data['class'] = klass

    update.message.reply_text('Inserisci l\'edizione:')

    return EDITION


def edition(update, context):
    edition = update.message.text
    context.chat_data['edition'] = edition

    update.message.reply_text('Ecco un riepilogo del tuo libro:\n*Titolo: *{title}\n*Autore: *{author}\n*Materia: *{subject}\n*Classe: *{klass}\n*Edizione: *{edition}'.format(
        title=context.chat_data['title'],
        author=context.chat_data['author'],
        klass=context.chat_data['class'],
        subject=context.chat_data['subject'],
        edition=context.chat_data['edition']
    ), parse_mode='markdown')
    update.message.reply_text(
        'Vuoi aggiungerlo?', reply_markup=confirm_keyboard_markup)

    return CONFIRM


def confirm(update, context):
    confirm = update.message.text
    if (confirm == 'Conferma ✅'):
        book = {key: context.chat_data[key] for key in ['book_id',
                                                        'title', 'author', 'class', 'subject', 'edition']}
        book['name'] = context.user_data['name']
        book['phone'] = context.user_data['phone']
        book['username'] = context.user_data['username']

        add_book(book)
        context.user_data['books'].append(book['book_id'])
        update.message.reply_text(
            'Libro aggiunto ✅\nUsa /lista per avere un elenco dei i tuoi libri')
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


add_entries = [CommandHandler('vendi', add)]
add_states = {
    TITLE: [MessageHandler(Filters.text & ~Filters.command, title)],
    AUTHOR: [MessageHandler(Filters.text & ~Filters.command, author)],
    SUBJECT: [MessageHandler(Filters.text & ~Filters.command, subject)],
    CLASS: [MessageHandler(Filters.text & ~Filters.command, klass)],
    EDITION: [MessageHandler(Filters.text & ~Filters.command, edition)],
    CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm)]
}
add_fallbacks = [CommandHandler(
    'annulla', cancel), MessageHandler(Filters.command, uknown)]

add_handler = ConversationHandler(
    entry_points=add_entries, states=add_states, fallbacks=add_fallbacks)
