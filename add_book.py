import pandas as pd


def add_book(book):
    books_df = pd.read_json('books.json')
    book_df = pd.DataFrame(book, index=[0])
    books_df.append(book_df, ignore_index=True).to_json('books.json')
