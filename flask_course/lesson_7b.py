from flask import Flask, render_template, make_response

app = Flask(__name__)


@app.route('/json/')
def json():
    return {'json': 42}     # Возвращает тип application/json


@app.route('/html/')
def html():
    return render_template('index.html')    # Возвращает тип text/html


@app.route('/not_found')
def not_found():
    return 'Oops!', 404


@app.errorhandler(404)
def not_found_page(error):
    return 'Unknown adress!', 404


@app.route('/foo', methods=['GET', 'POST', 'HEAD'])
def foo():
    response = make_response('foo')
    response.headers['X-Parachutes'] = 'parachutes are cool'  # noqa E501 Устанавливаем заголовок
    response.mimetype = 'text/plain'    # Меняем тип ответа
    response.status_code = 418		    # Задаем статус
    response.set_cookie('foo', 'bar')   # Устанавливаем cookie
    return response
