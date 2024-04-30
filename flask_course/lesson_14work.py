from flask import Flask, redirect, render_template, request

import os

from .data import Repository


def validate(data):
    errors = {}
    if not data.get('paid'):
        errors['paid'] = "Can't be blank"
    if not data.get('title'):
        errors['title'] = "Can't be blank"
    return errors


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


repo = Repository()


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/courses')
def courses_get():
    courses = repo.content()
    return render_template(
        'courses/index.html',
        courses=courses,
        )


# BEGIN (write your solution here)
@app.post('/courses')
def courses_post():
    course = request.form.to_dict()
    errors = validate(course)
    if errors:
        return render_template(
            'courses/new.html',
            course=course,
            errors=errors
        ), 422
    repo.save(course)
    return redirect('/courses', code=302)


@app.route('/courses/new')
def courses_new():
    course = {'paid': '', 'title': ''}
    errors = {}

    return render_template(
        'courses/new.html',
        course=course,
        errors=errors
    )
# END
