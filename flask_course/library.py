from flask import Flask, render_template, request, redirect, flash, \
    get_flashed_messages
import json

app = Flask(__name__)

app.secret_key = "secret_key"

books_ = {
    1: {
        'id': 1,
        'title': 'Pinocchio',
        'author': 'Carlo Collodi',
        'genre': 'fairy tale'
    },
}


def read_db(path='assets/books.json'):
    with open(path) as file:
        data = file.read()
    return json.loads(data)


def write_db(data, path='assets/books.json'):
    with open(path, 'w') as file:
        file.write(json.dumps(data))


def validate(data):
    errors = {}
    if not data.get('title'):
        errors['title'] = "Can't be blank"
    if not data.get('author'):
        errors['author'] = "Can't be blank"
    if not data.get('genre'):
        errors['genre'] = "Can't be blank"
    return errors


@app.route('/about')
def about():
    return render_template('library/about.html')


@app.route('/')
def root():
    return redirect('/books', code=302)


@app.get('/books')
def books():
    messages = get_flashed_messages(with_categories=True)
    books = list(read_db().values())
    return render_template(
        'library/index.html',
        books=books,
        messages=messages
    )


@app.post('/books')
def books_post():
    books = read_db()
    new_book = request.form.to_dict()
    errors = validate(new_book)
    if errors:
        return render_template(
            'library/new.html',
            book=new_book,
            errors=errors
        ), 422

    id = str(len(books) + 1)
    new_book['id'] = id
    books[f'{id}'] = new_book
    write_db(books)

    flash('Книга добавлена успешно', 'success')
    return redirect('/books', code=302)


@app.route('/books/new')
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
def book(id):
    books = read_db()
    return render_template(
        'library/show.html',
        book=books[id]
    )


@app.get('/books/<id>/edit')
def edit(id):
    books = read_db()
    book = books.get(id)
    errors = []

    return render_template(
           'library/edit.html',
           book=book,
           errors=errors,
    )


@app.route('/books/<id>/patch', methods=['POST'])
def patch_book(id):
    books = read_db()
    book = books.get(id)
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
    books[id] = book
    write_db(books)

    flash('Описание книги изменено успешно', 'success')
    return redirect('/books', code=302)
