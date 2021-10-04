from app import app

def test_hello_world():
  response = app.test_client().get('/')
  assert response.status_code == 200
  assert response.data == b'"hello world"\n'

def test_search():
  response = app.test_client().get('/search?term=xa')
  assert response.status_code == 200
  assert response.data == b'[{"author":"Ron Chernow","genre":"Non Fiction","id":19,"price":13,"reviews":'b'9198,"title":"Alexander Hamilton","user_rating":4.8,"year":2016}]\n'

def test_empty_search():
  response = app.test_client().get('/search?term=')
  assert response.status_code == 200
  assert len(response.data) == 94872

def test_autocomplete():
  response = app.test_client().get('/autocomplete?term=bab')
  assert response.status_code == 200
  assert response.data == b'[{"author":"DK","genre":"Non Fiction","id":28,"price":5,"reviews":5360,"title":"Baby Touch and Feel: Animals","user_rating":4.6,"year":2015}]\n'

def test_books():
  response = app.test_client().get('/books')
  assert response.status_code == 200
  assert len(response.data) == 94872

def test_users():
  response = app.test_client().get('/users')
  assert response.status_code == 200
  assert response.data == b'[{"id":0,"name":"Ada"},{"id":1,"name":"Zeke"},{"id":2,"name":"Fia"},{"id":3,"name":"Bob"}]\n'

def test_borrow_get():
  response = app.test_client().get('/borrow')
  assert response.status_code == 200
  assert response.data == b'[]\n'

def test_borrow_post():
  response = app.test_client().post('/borrow', json={'book_id': 7, 'user_id': 3})
  assert response.status_code == 200
  assert response.data == b'{"book_id":7,"user_id":3}\n'

def test_borrow_delete():
  response = app.test_client().delete('/borrow', json={'book_id': 7})
  assert response.status_code == 200
  assert response.data == b''


# error handling
def test_borrow_error():
  response = app.test_client().delete('/borrow')
  assert response.status_code == 404
  assert response.data == b'No user / book specified'

def test_borrow_error_post():
  response = app.test_client().post('/borrow', json={'book_id': 7, 'user_id': 3})
  response2 = app.test_client().post('/borrow', json={'book_id': 7, 'user_id': 3})
  assert response2.status_code == 403
  assert response2.data == b'book already borrowed'

def test_incorrect_route():
  response = app.test_client().get('/borrowww')
  assert response.status_code == 404
  assert response.data == b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>\n'
