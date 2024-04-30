from flask import Flask, render_template, request, redirect, flash, \
    get_flashed_messages
import json

app = Flask(__name__)

app.secret_key = "secret_key"

cars = [
    {'id': 1, 'name': 'BMW', 'city': 'Munchen', 'flagman': '7-series'},
    {'id': 2, 'name': 'Mersedes', 'city': 'Stuttgart', 'flagman': 'S-class'},
    {'id': 3, 'name': 'Audi', 'city': 'Ingolstadt', 'flagman': 'A8'},
    {'id': 4, 'name': 'VW', 'city': 'Wolfsburg', 'flagman': 'Phaeton'}
]
ids = {1: 0, 2: 1, 3: 2, 4: 3}


def read_db(path='assets/cars_db.json'):
    with open(path) as file:
        data = file.read()
    return json.loads(data)


def write_db(data, path='assets/cars_db.json'):
    with open(path, 'w') as file:
        file.write(json.dumps(data))


def validate(data):
    errors = {}
    if not data.get('name'):
        errors['name'] = "Can't be blank"
    if not data.get('city'):
        errors['city'] = "Can't be blank"
    if not data.get('flagman'):
        errors['flagman'] = "Can't be blank"
    return errors


@app.route('/')
def index():
    return render_template('cars/index.html')


@app.get('/cars')
def cars_get():
    messages = get_flashed_messages(with_categories=True)
    cars = read_db()
    return render_template(
        'cars/cars_list.html',
        cars=cars,
        messages=messages
    )


@app.post('/cars')
def cars_post():
    cars = read_db()
    car = request.form.to_dict()
    errors = validate(car)
    if errors:
        return render_template(
            'cars/new_car.html',
            car=car,
            errors=errors
        ), 422

    id_ = len(cars) + 1
    car['id'] = id_
    write_db(cars + [car])
    ids = read_db('assets/cars_ids_db.json')
    ids[f'{id_}'] = id_ - 1
    write_db(ids, 'assets/cars_ids_db.json')
    flash('Автокомпания добавлена успешно', 'success')
    return redirect('/cars', code=302)


@app.route('/cars/new')
def new_cars():
    car = {
        'name': '',
        'city': '',
        'flagman': ''
    }
    errors = {}
    return render_template(
        'cars/new_car.html',
        car=car,
        errors=errors
    )


@app.route('/cars/<int:id_>')
def car(id_):
    cars = read_db()
    ids = read_db('assets/cars_ids_db.json')
    return render_template(
        'cars/one_car.html',
        car=cars[ids[f'{id_}']].items()
    )
