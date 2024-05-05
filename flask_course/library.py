from flask import Flask, render_template, request, redirect, flash, \
    get_flashed_messages, session, url_for
from functools import wraps
from dotenv import load_dotenv
import json
import os
import sys
import uuid

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

PATH_TO_DATABASE = 'assets/books.json'
PATH_TO_AUTHBASE = 'assets/auth.json'

books_ = {      # sample book
    "839f6430-50f2-4131-91ec-9dace60754f1": {
        "id": "839f6430-50f2-4131-91ec-9dace60754f1",
        "title": "Pinocchio",
        "author": "Carlo Collodi",
        "genre": "fairy tale"
    },
}

users_ = {      # sample user
    "admin@libdb.ru": {
        "email": "admin@libdb.ru",
        "name": "admin",
        "password": "admin"
    },
}


class DB:
    def __init__(self, path_to_datafile):
        self.path = path_to_datafile

    def _read_db(self):
        with open(self.path) as file:
            return json.load(file)

    def _write_db(self, data):
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)

    def content(self):
        return self._read_db()

    def find(self, id):
        try:
            return self._read_db()[str(id)]
        except KeyError:
            sys.stderr.write(f'Wrong post id: {id}')
            raise

    def destroy(self, id):
        books = self._read_db()
        del books[id]
        self._write_db(books)


class LibDB(DB):
    def save(self, new_book):
        books = self._read_db()

        if not new_book.get('id'):
            new_id = str(uuid.uuid4())
            new_book['id'] = new_id

        books[new_book['id']] = new_book
        self._write_db(books)


class UserDB(DB):
    def save(self, new_user):
        users = self._read_db()
        email_new_user = new_user['email'].lower()
        new_user['email'] = email_new_user

        users.setdefault(email_new_user, {})
        users[email_new_user] = new_user

        self._write_db(users)


def validate(data, type='book'):
    type_valid = {
        'book': ['title', 'author', 'genre'],
        'user': ['email', 'name', 'password'],
        'login': ['email', 'password']
    }

    errors = {}

    for key in type_valid[type]:
        if not data.get(key):
            errors[key] = "Can't be blank"

    return errors


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not session.get('login', False):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view


@app.route('/about')
def about():
    return render_template('library/about.html')


@app.route('/')
def root():
    return redirect(url_for('books'), code=302)


@app.get('/books')
@login_required
def books():
    repo = LibDB(PATH_TO_DATABASE)
    messages = get_flashed_messages(with_categories=True)
    books = list(repo.content().values())
    return render_template(
        'library/index.html',
        books=books,
        messages=messages
    )


@app.post('/books')
@login_required
def books_post():
    repo = LibDB(PATH_TO_DATABASE)
    new_book = request.form.to_dict()
    errors = validate(new_book)
    if errors:
        return render_template(
            'library/new.html',
            book=new_book,
            errors=errors
        ), 422

    repo.save(new_book)

    flash('Книга добавлена успешно', 'success')
    return redirect(url_for('books'), code=302)


@app.route('/books/new')
@login_required
def new():
    book = {
        'title': '',
        'author': '',
        'genre': ''
    }
    errors = {}
    return render_template(
        'library/new.html',
        book=book,
        errors=errors
    )


@app.route('/books/<id>')
@login_required
def book(id):
    repo = LibDB(PATH_TO_DATABASE)
    book = repo.find(id)
    return render_template(
        'library/show.html',
        book=book
    )


@app.get('/books/<id>/edit')
@login_required
def edit(id):
    repo = LibDB(PATH_TO_DATABASE)
    book = repo.find(id)
    errors = []

    return render_template(
           'library/edit.html',
           book=book,
           errors=errors,
    )


@app.route('/books/<id>/patch', methods=['POST'])
@login_required
def patch_book(id):
    repo = LibDB(PATH_TO_DATABASE)
    book = repo.find(id)
    data = request.form.to_dict()

    errors = validate(data)
    if errors:
        return render_template(
            'library/edit.html',
            book=data,
            errors=errors
        ), 422

    for key in book:
        if key in data:
            book[key] = data[key]

    repo.save(book)

    flash('Описание книги изменено успешно', 'success')
    return redirect(url_for('books'), code=302)


@app.post('/books/<id>/delete')
@login_required
def delete_book(id):
    repo = LibDB(PATH_TO_DATABASE)
    repo.destroy(id)
    flash('Book has been deleted', 'success')
    return redirect(url_for('books'))


@app.get('/login')
def login():
    messages = get_flashed_messages(with_categories=True)
    user = {}
    errors = {}
    return render_template(
        'library/login.html',
        user=user,
        errors=errors,
        messages=messages
    )


@app.post('/login')
def login_post():
    repo = UserDB(PATH_TO_AUTHBASE)
    messages = get_flashed_messages(with_categories=True)
    auth_data = request.form.to_dict()
    errors = validate(auth_data, 'login')
    if errors:
        return render_template(
            'library/login.html',
            user=auth_data,
            messages=messages,
            errors=errors
        ), 422

    try:
        user = repo.find(auth_data['email'])
    except KeyError:
        flash('Неверный логин или пароль', 'error')
        return redirect(url_for('login'), code=302)

    if user['password'] != auth_data['password']:
        flash('Неверный логин или пароль', 'error')
        return redirect(url_for('login'), code=302)

    session['login'] = True
    flash('Успешный вход в систему', 'success')
    return redirect(url_for('books'), code=302)


@app.route('/logout')
@login_required
def logout_post():

    session['login'] = False
    session.clear()

    flash('Успешный выход из системы', 'success')
    return redirect(url_for('login'), code=302)


@app.post('/users')
@login_required
def new_user_post():
    repo = UserDB(PATH_TO_AUTHBASE)
    new_user = request.form.to_dict()
    errors = validate(new_user, 'user')
    if errors:
        return render_template(
            'library/new.html',
            book=new_user,
            errors=errors
        ), 422

    repo.save(new_user)

    flash('Пользователь добавлен успешно', 'success')
    return redirect(url_for('books'), code=302)


@app.route('/users/new')
@login_required
def new_user():
    user = {}
    errors = {}
    return render_template(
        'library/new_user.html',
        user=user,
        errors=errors
    )
