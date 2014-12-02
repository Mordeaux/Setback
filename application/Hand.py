import json
import time
from hashlib import sha1
from random import shuffle, choice

class Hand(object):

    def __init__(self, game_id=None):
        if not game_id:
            game_id = Hand.new_game()
        with open('games/'+game_id, 'r') as f:
            self.hand = json.loads(f.read())

    def save(self):
        with open('games/'+self['id'], 'w') as f:
            f.write(json.dumps(self.hand))

    def deal(self):
        for player in range(4):
            self['player'+str(player)] = [self['deck'].pop() for i in range(6)] 

    @staticmethod
    def new_game():
        with open('newhand.json') as f:
            hand = json.loads(f.read())
        shuffle(hand['deck'])
        # When I migrate to SQL this id choice will be prettier.
        game_id = sha1(str(time.time())+choice(hand['deck'])).hexdigest()
        hand['id'] = game_id
        with open('games/'+game_id, 'w') as f:
            f.write(json.dumps(hand))
        return game_id


    def __setitem__(self, key, value):
        self.hand[key] = value

    def __getitem__(self, key):
        return self.hand[key]


