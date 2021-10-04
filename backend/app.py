from flask import Flask, jsonify, request
from models import connect_db, Book, User, Borrow, db
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///chris_takehome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
@cross_origin()
@app.route('/')
def hello_world():
    return jsonify('hello world')

# search
@app.route('/search', methods=['GET'])
def search():
    term = request.args['term']
    return jsonify(Book.query.filter(Book.title.ilike(f'%{term}%')).all())

# auto complete
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
  term = request.args['term']
  return jsonify(Book.query.filter(Book.title.ilike(f'{term}%')).all())

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
    # GET
    if request.method == 'GET':
        # join query
        response = db.session.query(Book, User).filter(Borrow.book_id == Book.id, Borrow.user_id == User.id).all()
        result = []
        for item in response:
          print('item is', item)
          result.append({
            'title': item[Book]['title'],
            'id': item[Book]['id'],
            'user': item[User]['name']
          })
        return jsonify(result)

    else:
        json_body = request.get_json()
        if json_body == None:
            return 'No user / book specified', 404
        book = json_body['book_id'] if 'book_id' in json_body else None
        borrowed = Borrow.query.get(book)

        # POST
        if request.method == 'POST':
            if bool(borrowed) is False:
                user = json_body['user_id'] if 'user_id' in json_body else None
                response = Borrow.add(user, book)
                return jsonify(response)
            else:
                return 'book already borrowed', 403

        # DELETE
        if request.method == 'DELETE':

            print('deleting')
            if bool(borrowed) is True:
                response = Borrow.remove(borrowed)
                return '', 200
            else:
                return 'book not borrowed', 403
