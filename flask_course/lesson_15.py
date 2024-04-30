from flask import Flask, render_template

app = Flask(__name__)

cars = [
    {'id': 1, 'name': 'BMW', 'city': 'Munchen', 'flagman': '7-series'},
    {'id': 2, 'name': 'Mersedes', 'city': 'Stuttgart', 'flagman': 'S-class'},
    {'id': 3, 'name': 'Audi', 'city': 'Ingolstadt', 'flagman': 'A8'},
    {'id': 4, 'name': 'VW', 'city': 'Wolfsburg', 'flagman': 'Phaeton'}
]
ids = {1: 0, 2: 1, 3: 2, 4: 3}


@app.route('/')
def index():
    return render_template('cars/index.html')


@app.route('/cars')
def cars_page():
    return render_template(
        'cars/cars_list.html',
        cars=cars
    )


@app.route('/cars/<int:id>')
def car(id):
    return render_template(
        'cars/one_car.html',
        car=list(cars[ids[id]].items())[1:]
    )
