from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
import os
import json
import sys
import uuid
from flask import session


class PostsRepository():
    def __init__(self):
        if 'posts' not in session:
            session['posts'] = {}

    def content(self):
        return session['posts'].values()

    def find(self, id):
        try:
            return session['posts'][id]
        except KeyError:
            sys.stderr.write(f'Wrong post id: {id}')
            raise

    def destroy(self, id):
        del session['posts'][id]

    def save(self, post):
        if not (post.get('title') and post.get('body')):
            raise Exception(f'Wrong data: {json.loads(post)}')
        if not post.get('id'):
            post['id'] = str(uuid.uuid4())
        session['posts'][post['id']] = post
        session['posts'] = session['posts']
        return post['id']


def validate(post):
    errors = {}
    if not post.get('title'):
        errors['title'] = "Can't be blank"
    if not post.get('body'):
        errors['body'] = "Can't be blank"
    return errors


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/posts')
def posts_get():
    repo = PostsRepository()
    messages = get_flashed_messages(with_categories=True)
    posts = repo.content()
    return render_template(
        'posts/index.html',
        posts=posts,
        messages=messages,
        )


@app.route('/posts/new')
def new_post():
    post = {}
    errors = {}
    return render_template(
        'posts/new.html',
        post=post,
        errors=errors,
    )


@app.post('/posts')
def posts_post():
    repo = PostsRepository()
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'posts/new.html',
            post=data,
            errors=errors,
            ), 422
    id = repo.save(data)
    flash('Post has been created', 'success')
    resp = make_response(redirect(url_for('posts_get')))
    resp.headers['X-ID'] = id
    return resp


@app.route('/posts/<id>/update', methods=['GET', 'POST'])
def post_update(id):
    repo = PostsRepository()
    post = repo.find(id)
    errors = []

    if request.method == 'GET':
        return render_template(
                'posts/edit.html',
                post=post,
                errors=errors,
                data=post,
                )

    if request.method == 'POST':
        data = request.form.to_dict()

        errors = validate(data)
        if errors:
            return render_template(
                'posts/edit.html',
                post=post,
                data=data,
                errors=errors,
                ), 422

        post['title'] = data['title']
        post['body'] = data['body']
        repo.save(post)
        flash('Post has been updated', 'success')
        return redirect(url_for('posts_get'))


# BEGIN (write your solution here)
@app.post('/posts/<id>/delete')
def delete_post(id):
    repo = PostsRepository()
    repo.destroy(id)
    flash('Post has been removed', 'success')
    return redirect(url_for('posts_get'))
# END
