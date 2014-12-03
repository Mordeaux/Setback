import os
import json

from random import shuffle
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, current_user

from Game import Game
from User import User

from config import DIRECTORY, GAMES_DIR, USER_DIR, SECRET_KEY
from forms import LoginForm

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    validates = request.method == 'POST' and form.validate()
    if validates:
        username = request.form.get('username')
        password = request.form.get('password')
        if not User.username_taken(username):
            login_user(User(username=username, password=password))
            return redirect(request.args.get("next") or url_for("home"))
        elif User.check_password(User.id_from_name(username), request.form.get('password')):
            login_user(User(userid=User.id_from_name(username)))
            return redirect(request.args.get("next") or url_for("home"))
    return render_template('login.html', form=form)


@app.route('/')
@login_required
def home():
    return render_template('gameboard.html')


@app.route('/newgame')
@login_required
def new_game():
    pass

if __name__ == "__main__":
    app.run(debug=True)
