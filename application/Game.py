import json
from random import shuffle
from time import time

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from User import User
from config import Base
from CustomTypes import Json

class Trick(Base):
    __tablename__ = 'tricks'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    finished = Column(Boolean, default=False)
    turn = Column(Integer)
    last_mod = Column(Float)
    leading_suit = Column(Enum('h', 'd', 's', 'c'))
    trump = Column(Enum('h', 'd', 's', 'c'))
    table = Column(Json(28), default=['', '', '', ''])
    #You can't bid 1 in this game, so it is easy to check that everyone has bid
    #because the list will no longer contain a 1.
    #This bs hack will be fixed later though.
    bids = Column(Json(12), default=[1, 1, 1, 1])
    bidder = Column(Integer)

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
        return Game.query.get(game_id)

    def deal(self):
        self.trick = Trick(self)

    def __repr__(self):
        info = [player.username for player in self.players] + [self.id]
        # reorder these so teams are correct in __repr__
        info = (info[0], info[2], info[1], info[3], info[4])
        return '<%s + %s vs %s + %s, id:%r>' % info
