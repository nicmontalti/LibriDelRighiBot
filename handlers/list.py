from telegram.ext import CommandHandler, Filters
import pandas as pd


def df2str(df):
    string = ''
    for column in df.columns:
        string += '*'
        string += column
        string += ':* '
        string += df[column]
        string += '\n'
    return string


def list(update, context):
    book_ids = context.user_data['books']
    books = pd.read_json('../data/books.json')
    user_books = books.loc[book_ids]


df = pd.DataFrame([['ciao', 'boh'], ['2ciao', '2boh']], columns=['uno', 'due'])
print(df2str(df.loc[0]))
