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
        """Returns a dictionary that can be jsonified and sent to the client
           giving the client and used in Backbone to construct a Game model.
           This method must only give the client game state information which
           is meant to be available to the given User, ie. it must not reveal
           other player's hands, or cards which are in the discard pile."""
        print self.hand
        game = {
            'hand': self.hand,
            'id': self.game.id,
            'user_id': self.user.id,
            'play_to': self.game.play_to,
            'turn': self.trick.turn,
            'player_ids': [player.id for player in self.game.players],
            'usernames': [player.username for player in self.game.players],
            'team1_score': self.game.team1_score,
            'team2_score': self.game.team2_score,
            'last_mod': self.trick.last_mod,
            'leading_suit': self.trick.leading_suit,
            'trump': self.trick.trump,
            'table': self.trick.table,
            'player_number': self.player_number,
            'hands': [len(self.game.players_list[i].hand) for i in range(4)]
        }
        return game

    def is_fresh(self, timestamp):
        """This method allows the client to check to see if its copy of the 
           game state must be updated."""
        return timestamp == self.trick.last_mod

    def bid(self, bid):
        """Allows the user to enter a bid, as an integer."""
        # Until I figure out SQLAlchemy mutability issues for custom types
        # this will have to look like this
        # Also this currently does not check to make sure the player bids
        # at least 2, because empty bids are stored as 1 in the database,
        # so a bid of less than two will automatically be saved as a pass (0).
        bids = self.trick.bids
        if bid <= max(bids):
            bid = 0
        bids[self.player_number] = bid
        self.trick.bids = bids
        if 1 not in bids:
            self.trick.bidder = bids.index(max(bids))

    def set_trump(self, trump):
        """Checks that all bids are in, and that the User is the highest bidder
           then sets trump to the chosen suit."""
        self.trick.trump = trump

    def play_card(self, index):
        """Takes a numerical index and plays the card at that index."""
        if not (self.is_playable(index) and self.is_turn()):
            return 
        table = self.trick.table
        card = self.hand.pop(index)
        table[self.player_number] = card
        print table
        print id(table) == id(self.trick.table)

    def is_turn(self):
        """Checks to see that it is the User's turn to play a card or bid."""
        return True if self.trick.turn == self.player_number else False

    def is_playable(self, index):
        """Checks that it is possible to play a given card, according to the 
           rules of the game."""
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
