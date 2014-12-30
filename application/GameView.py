import json

from flask import jsonify

from config import db_session


class GameView(object):
    """Takes a User object and a Game object and provides methods to interact with that Game as that User."""

    def __init__(self, user=None, game=None):
        self.user = user
        self.game = game
        self.player_number = user.player_number(game)
        self.hand = game.players_list[self.player_number].hand
        self.trick = game.trick


    def view(self):
        game = {
            'hand': self.hand,
            'game_id': self.game.id,
            'user_id': self.user.id,
            'play_to': self.game.play_to,
            'turn': self.trick.turn,
            'player_ids': [player.id for player in self.game.players],
            'team1_score': self.game.team1_score,
            'team2_score': self.game.team2_score,
            'last_mod': self.trick.last_mod
        }
        return game

    def json(self):
        return jsonify(self.view())

    def respond(self, timestamp):
        return 304 if timestamp == self.trick.last_mod else self.json()
