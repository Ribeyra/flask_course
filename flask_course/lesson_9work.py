from flask import Flask, render_template

import random

from faker import Faker

SEED = 1234


def generate_users(users_count):
    fake = Faker()
    fake.seed_instance(SEED)

    ids = list(range(1, users_count))
    random.seed(SEED)
    random.shuffle(ids)

    users = []

    for i in range(users_count - 1):
        users.append({
            'id': ids[i],
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.free_email(),
        })

    return users


users = generate_users(100)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# BEGIN (write your solution here)
@app.route('/users')
def users_page():
    return render_template(
        'users/user_list.html',
        users=users
    )


@app.route('/users/<int:id>')
def user_page(id):
    user = next(filter(lambda x: x.get('id') == id, users), None)
    if user:
        return render_template(
            'users/show_user.html',
            user=user
        )
    return 'Page not found', 404
# END
