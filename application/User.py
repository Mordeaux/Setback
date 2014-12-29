import os
import json
import time

from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from config import DIRECTORY, hashulate, Base


class GamePlayers(Base):
    __tablename__ = 'players'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    player_number  = Column(Integer)
    player = relationship('User', backref=backref('games_list', cascade='all, delete-orphan'))
    game = relationship('Game', backref=backref('players_list', cascade='all, delete-orphan'))

    def __init__(self, game=None, user=None, player_number=None):
        self.game = game
        self.player = user
        self.player_number = player_number

    def __repr__(self):
        return '<Game %r, User %r, Number %r>' % (self.game_id, self.user_id, self.player_number)

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(40), nullable=False)
    current_game = Column(Integer, ForeignKey('games.id'))
    games = association_proxy('games_list', 'game')
 
    @staticmethod
    def get(userid):
        return User.query.filter(User.id == userid).first()

    @staticmethod
    def check_password(userid, password):
        user = User.query.filter(User.id == userid).first()
        if user.password == hashulate(password):
            return True
        return False

    def change_name(self, newname):
        self.username = newname
 
    def is_authenticated(self):
        """Returns True if the user is authenticated, i.e. they have provided 
        valid credentials. (Only authenticated users will fulfill the criteria 
        of login_required.)"""
        return True

    def is_active(self):
        """Returns True if this is an active user - in addition to being 
        authenticated, they also have activated their account, not been 
        suspended, or any condition your application has for rejecting an 
        account. Inactive accounts may not log in (without being forced of 
        course)."""
        return True

    def is_anonymous(self):
        """Returns True if this is an anonymous user. (Actual users should 
        return False instead.)"""
        return False

    def get_id(self):
        """Returns a unicode that uniquely identifies this user, and can be 
        used to load the user from the user_loader callback. Note that this 
        must be a unicode - if the ID is natively an int or some other type, 
        you will need to convert it to unicode."""
        return unicode(self.id)

    def __repr__(self):
        return '<User %r, id: %r>' % (self.username, self.id)

    def invite(self, game_id):
        pass
