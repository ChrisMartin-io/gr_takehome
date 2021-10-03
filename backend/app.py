from flask import Flask, jsonify, request
from models import connect_db, Book, User, Borrow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///chris_takehome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def hello_world():
  return jsonify('hello world')

# search
@app.route('/search', methods=['GET'])
def search():
  term = request.args['term']
  return jsonify(Book.query.filter(Book.title.ilike(f'%{term}%')).all())

# books
@app.route('/books', methods=['GET'])
def get_books():
  return jsonify(Book.query.all())

# users
@app.route('/users', methods=['GET'])
def get_users():
  return jsonify(User.query.all())

# methods for borrow
@app.route('/borrow', methods=['GET', 'POST', 'DELETE'])
def borrow():
  if request.method == 'GET':
    return jsonify(Borrow.query.all())

  else:
    json_body = request.get_json()
    user = json_body['user_id'] if 'user_id' in json_body else None
    book = json_body['book_id'] if 'book_id' in json_body else None
    borrowed = Borrow.query.get(book)

    print('borrowed is', borrowed)

    # POST
    if request.method == 'POST':
      if bool(borrowed) is False:
        response = Borrow.add(user, book)
        return jsonify(response) 
      else:
        return 'book already borrowed', 403

    # DELETE
    if request.method == 'DELETE':
      if bool(borrowed) is True:
        response = Borrow.remove(borrowed)
        return '', 200
      else:
        return 'book not borrowed', 403