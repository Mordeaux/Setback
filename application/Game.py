from random import shuffle
from time import time

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from User import User
from config import Base
from CustomTypes import Hand

class Trick(Base):
    """This ORM object stores the information relevant to a particular trick,
       which in setback is the section of a game that occurs between deals.
       The constructor of this obect takes care of dealing the cards."""
    __tablename__ = 'tricks'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    finished = Column(Boolean, default=False)
    turn = Column(Integer)
    last_mod = Column(Float)
    leading_suit = Column(Enum('h', 'd', 's', 'c'))
    trump = Column(Enum('h', 'd', 's', 'c'))
    #You can't bid 1 in this game, so it is easy to check that everyone has bid
    #because the list will no longer contain a 1.
    #This bs hack will be fixed later though.
    bidder = Column(Integer)
    winner0 = Column(Integer)
    winner1 = Column(Integer)
    winner2 = Column(Integer)
    winner3 = Column(Integer)
    winner4 = Column(Integer)
    winner5 = Column(Integer)

    def __init__(self, game):
        deck = [str(n)+s for s in ['d','h','s','c'] for n in range(2, 15)]
        shuffle(deck)
        game.players_list[0].hand = Hand(*[card for card in deck[:6]])
        game.players_list[1].hand = Hand(*[card for card in deck[6:12]])
        game.players_list[2].hand = Hand(*[card for card in deck[12:18]])
        game.players_list[3].hand = Hand(*[card for card in deck[18:24]])
        self.last_mod = time()
        self.turn = (game.dealer + 1) % 4


class Game(Base):
    """This ORM object holds all the information relevant to a particular 
       ongoing Game. Currently all Game logic is being stored in the 
       GameView object, in an attempt to separate logic and representation."""
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    finished = Column(Boolean, default=False)
    team1_score = Column(Integer, default=0)
    team2_score = Column(Integer, default=0)
    play_to = Column(Integer, default=21)
    dealer = Column(Integer, default=0)
    players = association_proxy('players_list', 'player')
    trick = relationship('Trick', backref='game', uselist=False)
    bids = association_proxy('players_list', 'bid')
    table = association_proxy('players_list', 'played_card')

    @staticmethod
    def get(game_id):
        """Returns a Game object given its id."""
        return Game.query.get(game_id)

    def deal(self):
        """Deals out a new Trick."""
        self.trick = Trick(self)

    def __repr__(self):
        info = [player.username for player in self.players] + [self.id]
        # reorder these so teams are correct in __repr__
        info = (info[0], info[2], info[1], info[3], info[4])
        return '<%s + %s vs %s + %s, id:%r>' % info
