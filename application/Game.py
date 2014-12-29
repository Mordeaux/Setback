import json
import os
import time
from hashlib import sha1
from random import shuffle, choice

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.associationproxy import association_proxy

from User import User, GamePlayers
from config import Base

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    finished = Column(Boolean)
    deck = Column(String(332))
    team1_score = Column(Integer)
    team2_score = Column(Integer)
    play_to = Column(Integer)
    turn = Column(Integer)
    players = association_proxy('players_list', 'player')

    @staticmethod
    def get(game_id):
        return Game.query.filter(Game.id == game_id).one()


    def __repr__(self):
        info = [player.username for player in self.players] + [self.id]
        # reorder these so teams are correct in __repr__
        info = (info[0], info[2], info[1], info[3], info[4])
        return '<%s + %s vs %s + %s, id:%r>' % tuple(info)
