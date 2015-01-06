from flask import jsonify

class GameView(object):
    """Takes a User object and a Game object and provides methods to interact with that Game as that User."""

    def __init__(self, user, game):
        self.user = user
        self.game = game
        self.player_number = user.player_number(game)
        self.hand = game.players_list[self.player_number].hand
        self.trick = game.trick
        print "GameView initializing: User %s game %s" % (str(user), str(game))

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
            'last_mod': self.trick.last_mod,
            'leading_suit': self.trick.leading_suit,
            'trump': self.trick.trump,
            'table': self.trick.table
        }
        return game

    def is_fresh(self, timestamp):
        return timestamp == self.trick.last_mod

    def bid(self, bid):
        # Until I figure out SQLAlchemy mutability issues for custom types
        # this will have to look like this
        bids = self.trick.bids
        if bid <= max(bids):
            bid = 0
        bids[self.player_number] = bid
        self.trick.bids = bids
        if 1 not in bids:
            self.trick.bidder = bids.index(max(bids))
        print type(bids)
        print bids

    def set_trump(self, trump):
        self.trick.trump = trump

    def play_card(self, index):
        if not (self.is_playable(index) and self.is_turn):
            return 
        table = self.trick.table
        card = self.hand.pop(index)
        table[player_number] = card
        print table
        print id(table) == id(self.trick.table)

    def is_turn(self):
        return True if self.trick.turn == self.player_number else False

    def is_playable(self, index):
        hand = self.hand
        trump = self.trick.trump
        leading_suit = self.trick.leading_suit
        playables = filter(lambda x: x[-1] in [leading_suit, trump], hand)
        if not playables:
            return True
        elif hand[index] in playables:
            return True
        else:
            return False
