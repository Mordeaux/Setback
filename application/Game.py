import json
from random import shuffle
from time import time

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from User import User, GamePlayers
from config import Base

class Trick(Base):
    __tablename__ = 'tricks'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    finished = Column(Boolean, default=False)
    turn = Column(Integer, ForeignKey('users.id'))
    last_mod = Column(Float)
    trump = Column(String(8))

    def __init__(self, game):
        deck = [str(n)+s for s in ['d','h','s','c'] for n in range(2, 15)]
        shuffle(deck)
        game.players_list[0].hand = json.dumps(deck[:6])
        game.players_list[1].hand = json.dumps(deck[6:12])
        game.players_list[2].hand = json.dumps(deck[12:18])
        game.players_list[3].hand = json.dumps(deck[18:24])
        self.last_mod = time()


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    finished = Column(Boolean, default=False)
    team1_score = Column(Integer, default=0)
    team2_score = Column(Integer, default=0)
    play_to = Column(Integer, default=21)
    players = association_proxy('players_list', 'player')
    trick = relationship('Trick', backref='game', uselist=False)

    @staticmethod
    def get(game_id):
        return Game.query.filter(Game.id == game_id).one()

    def deal(self):
        self.trick = Trick(self)

    def __repr__(self):
        info = [player.username for player in self.players] + [self.id]
        # reorder these so teams are correct in __repr__
        info = (info[0], info[2], info[1], info[3], info[4])
        return '<%s + %s vs %s + %s, id:%r>' % tuple(info)
