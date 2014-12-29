import json

from config import db_session


class GameView(object):
    """Takes a User object and a Game object and provides methods to interact with that Game as that User."""

    def __init__(self, user=None, game=None):
        self.user = user
        self.game = game
        self.player_number = user.player_number(game)
        self.hand = self.game.players_list[self.player_number].hand


    

    def json(self):
        response = {
            'cards': [],
            'game_id': self.game.id,
            'user_id': self.user.id,
            'play_to': self.game.play_to,
            'turn': self.game.turn,
            'player_ids': [player.id for player in self.game.players],
            'team1_score': self.game.team1_score,
            'team2_score': self.game.team2_score
        }
        return json.dumps(response)
