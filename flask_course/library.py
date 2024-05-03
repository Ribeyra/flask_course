from flask import Flask, render_template, request, redirect, flash, \
    get_flashed_messages, url_for
import json
import sys
import uuid

app = Flask(__name__)

app.secret_key = "secret_key"
PATH_TO_DATABASE = 'assets/books.json'

books_ = {      # sample book
    "839f6430-50f2-4131-91ec-9dace60754f1": {
        "id": "839f6430-50f2-4131-91ec-9dace60754f1",
        "title": "Pinocchio",
        "author": "Carlo Collodi",
        "genre": "fairy tale"
    },
}


class LibDB:
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

    def save(self, new_book):
        books = self._read_db()

        if not new_book.get('id'):
            new_id = str(uuid.uuid4())
            new_book['id'] = new_id

        books[new_book['id']] = new_book
        self._write_db(books)


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
    return redirect(url_for('books'), code=302)


@app.get('/books')
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
    repo = LibDB(PATH_TO_DATABASE)
    book = repo.find(id)
    return render_template(
        'library/show.html',
        book=book
    )


@app.get('/books/<id>/edit')
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
def delete_book(id):
    repo = LibDB(PATH_TO_DATABASE)
    repo.destroy(id)
    flash('Book has been deleted', 'success')
    return redirect(url_for('books'))
