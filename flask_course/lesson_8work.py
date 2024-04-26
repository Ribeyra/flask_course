from flask import Flask, jsonify

import random

from faker import Faker

SEED = 1234


def generate_companies(companies_count):
    fake = Faker()
    fake.seed_instance(SEED)

    ids = list(range(companies_count))
    random.seed(SEED)
    random.shuffle(ids)

    companies = []

    for i in range(companies_count):
        companies.append({
            "id": ids[i],
            "name": fake.company(),
            "phone": fake.phone_number(),
        })

    return companies


companies = generate_companies(100)

app = Flask(__name__)


@app.route('/')
def index():
    return 'open something like (you can change id): /companies/5'


@app.route('/companies/<id>')
def companies_page(id):
    res = list(filter(lambda x: x.get('id') == int(id), companies))
    if res:
        return jsonify(res[0])
    return 'Page not found', 404
