from flask import Flask, render_template, request

app = Flask(__name__)

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']


@app.route('/users')
def users_page():
    term = request.args.get('term', '')
    show_user = [user for user in users if term in user]
    return render_template(
        'users/index.html',
        users=show_user,
        search=term
    )
