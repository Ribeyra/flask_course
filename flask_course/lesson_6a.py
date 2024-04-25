from flask import Flask

# Это callable WSGI-приложение
app = Flask(__name__)


@app.get('/')
def hello_get():
    return 'Hello, GET!\n'


@app.post('/')
def hello_post():
    return 'Hello, POST!\n'
