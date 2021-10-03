from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from db import books_init, users_init
from dataclasses import dataclass

db = SQLAlchemy()

# initialize db, populate books and users
def connect_db(app):
    db.app = app
    db.init_app(app)
    books_init(db)
    users_init(db, app)


# classes: Book, User, BorrowedBooks
@dataclass
class Book(db.Model):
    id: int
    title: str
    author: str
    user_rating: float
    reviews: int
    price: int
    year: int
    genre: str

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, unique=True)
    author = db.Column(db.Text)
    user_rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    price = db.Column(db.Integer)
    year = db.Column(db.Integer)
    genre = db.Column(db.Text)

@dataclass
class User(db.Model):
    id: int
    name: str

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())

@dataclass
class Borrow(db.Model):
    user_id: str
    book_id: str

    __tablename__ = "borrowed_books"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)

    # add record
    def add(user, book):
      new_obj = Borrow(user_id=user, book_id=book)
      db.session.add(new_obj)
      db.session.commit()
      return Borrow.query.get(book)


    # remove record
    def remove(book):
      print('book is', book)
      Borrow.query.filter('book_id' == book.book_id).delete()
      return True