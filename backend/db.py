import pandas as pd

# initialize books table
# drop pre-existing tables
# populate data from csv using pandas
# ensure primary key active on books table
def books_init(db):
    engine = db.get_engine()
    csv_file_path = 'books2.csv'
    con = engine.connect()

    con.execute('DROP TABLE IF EXISTS borrowed_books, books, users, bborrowed')
    with open(csv_file_path, 'r') as file:
        csv_data = pd.read_csv(file)
    csv_data.to_sql('books',
                    con=engine,
                    index=True,
                    index_label='id',
                    if_exists='replace')

    con.execute('ALTER TABLE books ADD PRIMARY KEY (id);')
    db.create_all()

# init users table, add users
def users_init(db, app):
    from models import User
    with app.app_context():
        db.session.add(User(name='Ada', id=0))
        db.session.add(User(name='Zeke', id=1))
        db.session.add(User(name='Fia', id=2))
        db.session.add(User(name='Bob', id=3))
        db.session.commit()