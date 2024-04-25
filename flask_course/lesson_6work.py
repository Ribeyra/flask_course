from faker import Faker
from flask import Flask, jsonify

fake = Faker()
fake.seed_instance(1234)

domains = [fake.domain_name() for i in range(10)]
phones = [fake.phone_number() for i in range(10)]

app = Flask(__name__)


@app.route('/')
def index():
    return 'go to the /phones or /domains'


# BEGIN (write your solution here)
@app.route('/phones')
def phones_page():
    return jsonify(phones)


@app.route('/domains')
def domains_page():
    return jsonify(domains)
# END
