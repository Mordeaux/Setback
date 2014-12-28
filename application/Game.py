import json
import os
import time
from hashlib import sha1
from random import shuffle, choice

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from User import User
from config import GAMES_DIR, Base

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    finished = Column(Boolean)
    deck = Column(String(332))
    team1_score = Column(Integer)
    team2_score = Column(Integer)
    player0_id = Column(Integer, ForeignKey('users.id'))
    player1_id = Column(Integer, ForeignKey('users.id'))
    player2_id = Column(Integer, ForeignKey('users.id'))
    player3_id = Column(Integer, ForeignKey('users.id'))
    
 
    def __init__(self, game_id=None):
        if not game_id:
            game_id = Game.new_game()
        with open(os.path.join(GAMES_DIR, game_id), 'r') as f:
            self.game = json.loads(f.read())
        self.id = game_id

    def save(self):
        with open(os.path.join(GAME_DIR, self['id']), 'w') as f:
            f.write(json.dumps(self.game))

    def deal(self):
        self['deck'].append(self['team1_discards'])
        self['deck'].append(self['team2_discards'])
        self['team1_discards'] = []
        self['team2_discards'] = []
        shuffle(self['deck'])
        for player in range(4):
            self['player'+str(player)] = [self['deck'].pop() for i in range(6)] 

    def invite(self, user_id):
        if len(self['players']) < 4:
            self['players'].append(user_id)
        with User(userid=user_id) as user:
            user['invites'].append(self['id'])

    @staticmethod
    def new_game():
        with open('newgame.json') as f:
            game = json.loads(f.read())
        # When I migrate to SQL this id choice will be prettier.
        game_id = sha1(str(time.time())+choice(game['deck'])).hexdigest()
        game['id'] = game_id
        with open(os.path.join(GAMES_DIR, game_id), 'w') as f:
            f.write(json.dumps(game))
        return game_id

    def model(self, user_id):
        player = 'player'+str(self['players'].index(user_id))
        response = {
            'cards': self[player],
            'id': self['id'],
            'play_to': self['play_to'],
            'turn': self['turn'],
            'players': self['players']
        }
        return json.dumps(response)

    def __setitem__(self, key, value):
        self.game[key] = value

    def __getitem__(self, key):
        return self.game[key]

    def __enter__(self):
        return self

    def __exit__(self):
        self.save()

