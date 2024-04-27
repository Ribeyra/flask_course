from flask import render_template, Flask

app = Flask(__name__)


@app.route('/users/<id>')
def users(id):

    return render_template(
        'index.html',
        name=id,
    )


def get_courses():
    return [
        {'name': 'Верстка', 'id': 5},
        {'name': 'ООП', 'id': 7},
        {'name': 'HTTP', 'id': 22},
        {'name': 'SQL', 'id': 12}
    ]


""" @app.route('/courses/')
def courses():
    courses = get_courses()
    # Возвращает список курсов, которые представлены словарем

    return render_template(
        'courses/view.html',
        courses=courses
    )


@app.route('/courses_list/')
def courses_list():
    courses = get_courses()
    # Возвращает список курсов, которые представлены словарем

    return render_template(
        'courses/view_list.html',
        courses=courses
    ) """


@app.route('/courses/')
def courses():
    courses = get_courses()
    # Возвращает список курсов, которые представлены словарем

    return render_template(
        'courses.html',
        courses=courses
    )


@app.route('/courses_list/')
def courses_list():
    courses = get_courses()
    # Возвращает список курсов, которые представлены словарем

    return render_template(
        'courses/view_list.html',
        courses=courses
    )
