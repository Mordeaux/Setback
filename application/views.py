import os
import json

from random import shuffle
from flask import Flask, render_template, request, redirect, url_for
from flask import session, has_request_context
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
        print 'getting game view'
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
            login_user(User(username=username, password=password))
            return redirect(request.args.get("next") or url_for("home"))
        elif User.check_password(User.id_from_name(username), 
                                 request.form.get('password')):
            login_user(User(userid=User.id_from_name(username)))
            return redirect(request.args.get("next") or url_for("home"))
    return render_template('login.html', form=form)


@app.route('/')
@login_required
def home():
    return render_template('dashboard.html', user=current_user)


@app.route('/newgame')
@login_required
def new_game():
    pass


@app.route('/game')
@login_required
def games():
    return current_user.current_games()


@app.route('/game/<int:game_id>', methods=['PUT', 'POST', 'GET'])
@login_required
def game(game_id):
    print game_id


@app.route('/user/<int:user_id>')
def name_from_id(user_id):
    return User.get(user_id).username


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.before_first_request
def setup():
    if not os.path.isfile(os.path.join(DIRECTORY, 'test.db')):
        init_db()
    mike = User(username='mordo', password=hashulate('password'))
    kait = User(username='kaitlin', password=hashulate('password'))
    josh = User(username='josh', password=hashulate('password'))
    nat = User(username='natalia', password=hashulate('password'))
    game = Game()
    mike.join_game(game, 0)
    kait.join_game(game, 1)
    josh.join_game(game,2)
    nat.join_game(game, 3)
    db_session.add(mike)
    db_session.add(kait)
    db_session.add(josh)
    db_session.add(nat)
    game.deal()
    db_session.commit()
    print 'break-----------------------'
    print User.query.all()
    print 'break-----------------------'
    print User.query.filter(User.id == 1).one()
    print 'break-----------------------'
    print Game.query.all()
    print 'break-----------------------'
    print User.get(1)
    print 'break-----------------------'
    print User.get(1).games
    print 'break-----------------------'
    print mike.games
    print 'break-----------------------'
    print mike.games[0].players
    print 'break-----------------------'
    view = GameView(mike, game)
    print view.player_number
    print 'break-----------------------'
    print view.json()
    print 'break-----------------------'
    print game.players_list
    print 'break-----------------------'
    print game.players_list[0].user_id
    print 'break-----------------------'
    for player in game.players_list:
        print 'Player id:%r' % player.user_id
        print 'Hand: %s' % player.hand
        print 'break-----------------------'
    print view.hand
    print 'break-----------------------'




if __name__ == "__main__":
    app.run(debug=True)
