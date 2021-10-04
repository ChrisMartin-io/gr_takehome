from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
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
    def __getitem__(self, title):
        return self.__dict__[title]
    def __getitem__(self, id):
        return self.__dict__[id]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, unique=True)
    author = db.Column(db.Text)
    user_rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    price = db.Column(db.Integer)
    year = db.Column(db.Integer)
    genre = db.Column(db.Text)
    users = relationship('User', secondary = 'borrowed_books')

@dataclass
class User(db.Model):
    id: int
    name: str

    __tablename__ = "users"
    def __getitem__(self, name):
        return self.__dict__[name]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    books = relationship('Book', secondary = 'borrowed_books', overlaps='users')


@dataclass
class Borrow(db.Model):
    user_id: str
    book_id: str

    __tablename__ = "borrowed_books"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),
                        primary_key=True)

    # add borrowed book
    def add(user, book):
        new_obj = Borrow(user_id=user, book_id=book)
        db.session.add(new_obj)
        db.session.commit()
        return Borrow.query.get(book)

    # remove borrowed book
    def remove(book):
        new_obj = Borrow.query.filter_by(book_id=book.book_id).first()
        db.session.delete(new_obj)
        db.session.commit()
        return True

