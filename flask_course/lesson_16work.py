from flask import Flask, render_template, request
from faker import Faker

fake = Faker()
Faker.seed(1234)


def generate(size):
    posts = []
    for _ in range(size):
        posts.append({
            'id': fake.uuid4(),
            'title': fake.sentence(),
            'body': fake.text(),
            'slug': fake.slug(),
            })
    return posts


class PostsRepository:
    def __init__(self, size):
        self.posts = generate(size)

    def content(self):
        return self.posts

    def find(self, slug):
        return next(
            (post for post in self.posts if slug == post['slug']),
            None
        )


app = Flask(__name__)
repo = PostsRepository(50)


@app.route('/')
def index():
    return render_template('posts/index.html')


# BEGIN (write your solution here)
@app.route('/posts')
def posts():
    all_posts = repo.content()
    page = request.args.get('page', 1, type=int)
    PER = 5
    begin = (page - 1) * PER
    end = begin + PER
    result = all_posts[begin:end]
    return render_template(
        'posts/index.html',
        posts=result,
        page=page
    )


@app.route('/posts/<slug>')
def show_post(slug):
    post = repo.find(slug)
    if post is None:
        return 'Page not found', 404
    return render_template(
        'posts/show.html',
        post=post
    )
# END
