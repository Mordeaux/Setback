"""
To do:
- Switch to websockets
  -Miguel Greenberg's FlaskSocketIO?
    -Won't work on Dreamhost apparantly?
- Switch all hacky json lists to tables
"""

import os

from random import shuffle
from flask import Flask, render_template, request, redirect, url_for
from flask import session, has_request_context, jsonify
from flask.ext.login import LoginManager, login_required, login_user
from flask.ext.login import current_user, logout_user, AnonymousUserMixin
from werkzeug.local import LocalProxy

from Game import Game
from User import User, GamePlayers
from GameView import GameView
from config import DIRECTORY, SECRET_KEY, db_session, hashulate, init_db
from forms import LoginForm

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

game_view = LocalProxy(lambda:get_game_view())

def get_game_view():
    if has_request_context() and current_user.is_authenticated():
        if request.args.get('game'):
            session['current_game'] = request.args.get('game')
        if session.get('current_game', False):
            return current_user.view(Game.get(session['current_game']))
    return None


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    validates = request.method == 'POST' and form.validate()
    if validates:
        username = request.form.get('username')
        password = request.form.get('password')
        if not User.username_taken(username):
            user = User(username=username, password=password)
            db_session.add(user)
            db_session.commit()
            login_user(user)
            return redirect(request.args.get("next") or url_for("home"))
        elif User.check_password(User.id_from_name(username), 
                                 request.form.get('password')):
            login_user(User(id=User.id_from_name(username)))
            return redirect(request.args.get("next") or url_for("home"))
    return render_template('login.html', form=form)


@app.route('/')
@login_required
def home():
    return render_template('dashboard.html', user=current_user)


@app.route('/game', methods=['GET', 'POST'])
@login_required
def games():
    if request.method == 'GET':
        return jsonify(current_user.current_games())
    elif request.method == 'POST':
        game = Game()
        player1 = request.form.get('player1')
        player2 = request.form.get('player2')
        player3 = request.form.get('player3')
        player4 = request.form.get('player4')
        User.get(player1).join_game(game, 1)
        User.get(player2).join_game(game, 2)
        User.get(player3).join_game(game, 3)
        User.get(player4).join_game(game, 4)
        session['current_game'] = game.id
        return jsonify(game_view.view())


@app.route('/game/<int:game_id>', methods=['POST', 'GET'])
@login_required
def game(game_id):
    session['current_game'] = game_id
    if request.method == 'GET':
        time = request.args.get('timestamp')
        return jsonify(game_view.view()) if game_view.is_fresh(time) else 304
    elif request.method == 'POST':
        card_index = request.form.get('card_index')
        game_view.play_card(card_index)
        return jsonify(game_view.view())


@app.route('/user')
@login_required
def get_users():
    return jsonify(User.get_users())


@app.route('/user/<int:user_id>')
@login_required
def name_from_id(user_id):
    if current_user.id == user_id:
        return jsonify(current_user.model())
    return User.get(user_id).username


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.before_first_request
def setup():
    if not os.path.isfile(os.path.join(DIRECTORY, 'test.db')):
        init_db()


@app.route('/test')
@login_required
def test():
    mike = User.get(1)
    kait = User(username='kaitlin', password=hashulate('password'))
    josh = User(username='josh', password=hashulate('password'))
    nat = User(username='natalia', password=hashulate('password'))
    game = Game()
    mike.join_game(game, 0)
    kait.join_game(game, 1)
    josh.join_game(game,2)
    nat.join_game(game, 3)
#    db_session.add(mike)
#    db_session.add(kait)
#    db_session.add(josh)
#    db_session.add(nat)
    game.deal()
    db_session.commit()
    viewm = mike.view(game)
    viewk = kait.view(game)
    viewj = josh.view(game)
    viewn = nat.view(game)
    viewm.bid(0)
    viewk.bid(2)
    viewj.bid(3)
    viewn.bid(0)
    viewj.set_trump('h')
#    db_session.add(mike)
    db_session.commit()
    return "SUCCESS"

@app.route('/test1')
@login_required
def test1():
    mike = User.get(1)
    kait = User.get(2)
    josh = User.get(3)
    nat = User.get(4)    
    game = game.get(1)
    viewm = mike.view(game)
    viewk = kait.view(game)
    viewm = josh.view(game)
    viewm = nat.view(game)
    viewj.play_card(2)

if __name__ == "__main__":
    app.run(debug=True)
