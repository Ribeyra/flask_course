from flask import Flask

app = Flask(__name__)


@app.route('/users/<id>')
def users(id):
    return f'This user has id:{id}'
