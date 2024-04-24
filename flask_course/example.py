from flask import Flask

# Это callable WSGI-приложение
app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Градиентный фон</title>
<style>
  body {
    margin: 0;
    padding: 0;
    background: linear-gradient(45deg, yellow, pink);
    background-size: cover;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
</head>
<body>
</body>
</html>
"""


@app.route('/')
def hello_world():
    return html


@app.route('/home/')
def hello_home():
    return 'Welcome to Home!'
