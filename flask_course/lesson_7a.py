from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    print(request.headers)  # Выводит все заголовки
    return 'Hello, World!'


@app.route('/users/')
def users():
    print(request.args)  # => {'page': 12, 'per': 5}
    page = request.args.get('page', 1)
    per = request.args.get('per', 10, type=int)
    response = make_response(f'page: {page}, per: {per}')
    return response


@app.post('/user')
def user():
    return 'Users', 302
