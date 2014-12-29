import os
import json

from random import shuffle
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user

from Game import Game
from User import User, GamePlayers

from config import DIRECTORY, SECRET_KEY, db_session, hashulate, init_db
from forms import LoginForm


app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


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


@app.route('/game/<int:idno>', methods=['PUT', 'POST', 'GET'])
@login_required
def game(idno):
    print idno


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
    game2 = Game()
    GamePlayers(game, mike, 0)
    GamePlayers(game, josh, 1)
    GamePlayers(game, kait, 2)
    GamePlayers(game, nat, 3)
    GamePlayers(game2, mike, 3)
    GamePlayers(game2, josh, 2)
    GamePlayers(game2, kait, 1)
    GamePlayers(game2, nat, 0)
#    mike.games.append(game)
#    kait.games.append(game)
#    josh.games.append(game)
#    nat.games.append(game)
    db_session.add(mike)
    db_session.add(kait)
    db_session.add(josh)
    db_session.add(nat)
    db_session.add(game)
#    db_session.add(game2)
#    db_session.add(games1)
#    db_session.add(games2)
#    db_session.add(games3)
#    db_session.add(games0)
#    db_session.add(games0)
#    db_session.add(games1)
#    db_session.add(games2)
#    db_session.add(games3)
    db_session.commit()
    print 'break-----------------------'
    print game == game2
    print 'break-----------------------'
    print User.query.all()
    print 'break-----------------------'
    print Game.query.all()
    print 'break-----------------------'
    print User.get(1)
    print 'break-----------------------'
    print User.get(1).games
    print 'break-----------------------'
    print mike.games
    print 'break-----------------------'
    print kait.games_list[0].player_number
    print 'break-----------------------'
    print mike.username
    mike.change_name('bjork')
    print 'break-----------------------'
    print mike.username
    print 'break-----------------------'
    print mike.games[0].players


if __name__ == "__main__":
    app.run(debug=True)
    print User.get(1).username
