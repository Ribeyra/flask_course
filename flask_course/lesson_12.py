from flask import Flask, render_template, request

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
    term = request.args.get('term', '')
    if not term:
        show_user = users
    else:
        show_user = [
            user for user in users
            if (user['first_name'].lower()).startswith(term.lower())
        ]
    return render_template(
        'users/index2.html',
        users=show_user,
        search=term
    )
# END
