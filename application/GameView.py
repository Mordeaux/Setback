import json

from config import db_session


class GameView(object):
    """Takes a User object and a Game object and provides methods to interact with that Game as that User."""

    def __init__(self, user=None, game=None):
        self.user = user
        self.game = game


    

    def json(self):
        response = {
            'cards': [],
            'id': self.game.id,
            'play_to': self.game.play_to,
            'turn': self.game.turn,
            'players': self.game.ordered_usernames()
        }
