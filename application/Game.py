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
    players = association_proxy('players_list', 'player')


    def __repr__(self):
        info = tuple([player.username for player in self.players]+[self.id])
        return '<%s and %s versus %s and %s, id:%r>' % info
