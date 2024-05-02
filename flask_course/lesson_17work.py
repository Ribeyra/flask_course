from flask import ( # noqa f401
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

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


def validate(post):
    errors = {}
    if not post.get('title'):
        errors['title'] = "Can't be blank"
    if not post.get('body'):
        errors['body'] = "Can't be blank"
    return errors


app = Flask(__name__)

app.secret_key = "secret_key"


@app.route('/')
def index():
    return render_template('posts2/index_root.html')


@app.get('/posts')
def posts_get():
    repo = PostsRepository()
    messages = get_flashed_messages(with_categories=True)
    posts = repo.content()
    return render_template(
        'posts2/index.html',
        posts=posts,
        messages=messages
    )


# BEGIN (write your solution here)
@app.get('/posts/new')
def new_post():
    post = {}
    errors = {}
    return render_template(
        'posts2/new.html',
        post=post,
        errors=errors
    )


@app.post('/posts')
def posts_post():
    repo = PostsRepository()
    new_post = request.form.to_dict()
    errors = validate(new_post)
    if errors:
        return render_template(
            'posts2/new.html',
            post=new_post,
            errors=errors
        ), 422
    repo.save(new_post)
    flash('Post has been created', 'success')
    return redirect(url_for('posts_get'), 302)
# END
