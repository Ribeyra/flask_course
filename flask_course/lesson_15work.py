from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    redirect,
    url_for
)
import os   # noqa F401

app = Flask(__name__)
app.secret_key = "secret_key"


# BEGIN (write your solution here)
@app.post('/courses')
def courses():
    flash('Course Added', 'success')
    return redirect(url_for('index'), code=302)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )
# END
