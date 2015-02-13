from random import shuffle
from time import time

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship, backref, composite
from sqlalchemy.ext.associationproxy import association_proxy

from User import User
from config import Base
from CustomTypes import Hand, Discards

class Team1(Base):
    __tablename__ = 'team_1'
    id = Column(Integer, primary_key=True)
    card0 = Column(String(3))
    card1 = Column(String(3))
    card2 = Column(String(3))
    card3 = Column(String(3))
    cards = composite(Discards, card0, card1, card2, card3)
    trick_id = Column(Integer, ForeignKey('tricks.id'))
    trick = relationship('Trick',
                        backref=backref('team1_discards',
                                        cascade='all, delete-orphan'))

    def __init__(self, discards):
        self.cards = Discards(*discards)

class Team2(Base):
    __tablename__ = 'team_2'
    id = Column(Integer, primary_key=True)
    card0 = Column(String(3))
    card1 = Column(String(3))
    card2 = Column(String(3))
    card3 = Column(String(3))
    cards = composite(Discards, card0, card1, card2, card3)
    trick_id = Column(Integer, ForeignKey('tricks.id'))
    trick = relationship('Trick',
                        backref=backref('team2_discards',
                                        cascade='all, delete-orphan'))

    def __init__(self, discards):
        self.cards = Discards(*discards)

class Trick(Base):
    """This ORM object stores the information relevant to a particular trick,
       which in setback is the section of a game that occurs between deals.
       The constructor of this obect takes care of dealing the cards."""
    __tablename__ = 'tricks'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    finished = Column(Boolean, default=False)
    turn = Column(Integer)
    last_mod = Column(Integer)
    leading_suit = Column(Enum('h', 'd', 's', 'c'))
    trump = Column(Enum('h', 'd', 's', 'c'))
    #You can't bid 1 in this game, so it is easy to check that everyone has bid
    #because the list will no longer contain a 1.
    #This bs hack will be fixed later though.
    bidder = Column(Integer)
    team1 = association_proxy('team1_discards', 'cards')
    team2 = association_proxy('team2_discards', 'cards')

    def __init__(self, game):
        deck = [str(n)+s for s in ['d','h','s','c'] for n in range(2, 15)]
        shuffle(deck)
        for i in range(len(game.hands)):
            game.hands[i] = Hand(*deck[i*6:(i+1)*6])
        self.last_mod = int(time())
        self.turn = (game.dealer + 1) % 4
        for hand in game.hands:
            if not filter(None, map(lambda x: int(x[:-1])>=10, hand)):
                game.deal()
                break
        for i in range(4):
            game.bids[i] = 1

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
    hands = association_proxy('players_list', 'hand')
    message = Column(String, default='')

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

    def __str__(self):
        info = [player.username for player in self.players]
        info = (info[0], info[2], info[1], info[3], 
                self.team1_score, self.team2_score)
        return '%s and %s versus %s and %s:<br>Score %d:%d' % info
