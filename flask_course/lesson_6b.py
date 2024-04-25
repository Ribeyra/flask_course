from flask import Flask, request

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    match request.method:
        case 'POST':
            return 'Hello, POST!\n'
        case 'GET':
            return 'Hello, GET!\n'
        case _:
            return 'Unknown mothod\n'
