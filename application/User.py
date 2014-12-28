import os
import json
import time

from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from config import DIRECTORY, USER_DIR, hashulate, Base


class Friends(Base):
    __tablename__ = 'friends'
    left_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    friend = relationship("User", backref="parent_assocs")

class Association(Base):
    __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    player_number  = Column(Integer)
    game = relationship("Game", backref="parent_assocs")

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(40), nullable=False)
    email = Column(String(50), nullable=False)
    games = relationship('Association', backref='users')
 
    @staticmethod
    def get(userid):
        return User.query.filter(User.id == userid).first()

    @staticmethod
    def check_password(userid, password):
        user = User.query.filter(User.id == userid).first()
        if user.password == hashulate(password):
            return True
        return False
 
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
