import pandas as pd

df = pd.DataFrame(columns=['id', 'title', 'author',
                  'edition', 'class', 'subject', 'name', 'phone', 'username'])

df.to_json('books.json')
