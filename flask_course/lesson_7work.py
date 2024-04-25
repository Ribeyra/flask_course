from flask import Flask, jsonify, request

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
            "name": fake.company(),
            "phone": fake.phone_number(),
        })
    return companies


companies = generate_companies(100)

app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='/companies'>Companies</a>"


# BEGIN (write your solution here)
@app.route('/companies')
def companies_page():
    page = request.args.get('page', 1, type=int)
    per = request.args.get('per', 5, type=int)
    begin = (page - 1) * per
    end = begin + per
    result = companies[begin:end]
    return jsonify(result)
# END
