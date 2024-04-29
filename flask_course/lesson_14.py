from flask import Flask, render_template, request, redirect
import re
import json

app = Flask(__name__)


def read_db(path='assets/db.json'):
    with open(path) as file:
        data = file.read()
    return json.loads(data)


def write_db(data, path='assets/db.json'):
    with open(path, 'w') as file:
        file.write(json.dumps(data))


def validate(data) -> dict:
    errors = {}
    nick_pattern = r'^[a-zA-Z0-9_-]{3,16}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,5}$'
    if not re.match(nick_pattern, data['nickname']):
        errors['nickname'] = "Никнейм не валиден"
    if not re.match(email_pattern, data['email']):
        errors['email'] = "Email не валиден"
    return errors


@app.route('/users/new')
def new_user():
    user = {
        'nickname': '',
        'email': ''
    }
    errors = {}

    return render_template(
        'users/new.html',
        user=user,
        errors=errors
    )


@app.post('/users')
def users_post():
    users = read_db()
    users_count = len(users)
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
          'users/new.html',
          user=user,
          errors=errors,
        ), 422
    user['id'] = users_count + 1
    write_db(users + [user])
    return redirect('/users', code=302)


@app.route('/users')
def show_users():
    users = read_db()
    return render_template(
        'users/users_list.html',
        users=users
    )
