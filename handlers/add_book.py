import pandas as pd


def add_book(book):
    books_df = pd.read_json('../data/books.json')
    book_df = pd.DataFrame(book, index=book['book_id'])
    books_df.append(book_df, ignore_index=False).to_json('books.json')
