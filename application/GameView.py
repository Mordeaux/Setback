from time import time

from flask import jsonify

from CustomTypes import Discards

class GameView(object):
    """Takes a User object and a Game object and provides methods to interact with that Game as that User."""

    def __init__(self, user, game):
        self.user = user
        self.game = game
        self.player_number = user.player_number(game)
        self.hand = game.hands[self.player_number]
        self.trick = game.trick
        self.bids = game.bids
        self.turn = self.trick.turn
        self.f = lambda x: len(filter(None, x))

    def view(self):
        """Returns a dictionary that can be jsonified and sent to the client
           giving the client and used in Backbone to construct a Game model.
           This method must only give the client game state information which
           is meant to be available to the given User, ie. it must not reveal
           other player's hands, or cards which are in the discard pile."""
        game = {
            'hand': filter(None, self.hand),
            'id': self.game.id,
            'user_id': self.user.id,
            'play_to': self.game.play_to,
            'turn': self.turn,
            'player_ids': [player.id for player in self.game.players],
            'usernames': [player.username for player in self.game.players],
            'team1_score': self.game.team1_score,
            'team2_score': self.game.team2_score,
            'last_mod': self.trick.last_mod,
            'leading_suit': self.trick.leading_suit,
            'trump': self.trick.trump,
            'table': list(self.game.table),
            'player_number': self.player_number,
            'hands': [self.f(self.game.hands[i]) for i in range(4)],
            'bid': None if 1 in self.game.bids else max(self.game.bids),
            'bidder': self.trick.bidder,
            'bids': list(self.bids)
        }
        return game

    def is_fresh(self, timestamp):
        """This method allows the client to check to see if its copy of the 
           game state must be updated."""
        return timestamp == self.trick.last_mod

    def bid(self, bid):
        """Allows the user to enter a bid, as an integer."""
        # Also this currently does not check to make sure the player bids
        # at least 2, because empty bids are stored as 1 in the database,
        # so a bid of less than two will automatically be saved as a pass (0).
        dealer_bid_4 = self.player_number == self.game.dealer and bid == 4
        if self.is_turn():
            if bid <= max(self.bids) and not dealer_bid_4:
                bid = 0
            self.bids[self.player_number] = bid
            if 1 not in self.bids:
                self.trick.bid = max(self.bids)
                if dealer_bid_4:
                    self.trick.bidder = self.game.dealer
                else:
                    self.trick.bidder = list(self.bids).index(max(self.bids))
                self.bidding_finished()
            else:
                self.changed()

    def set_trump(self, trump):
        """Checks that all bids are in, and that the User is the highest bidder
           then sets trump to the chosen suit."""
        if not self.trick.trump and self.trick.bidder == self.player_number:
            self.trick.trump = trump
            self.bidding_finished()

    def play_card(self, card):
        """Takes a card and plays it."""
        if self.is_playable(card) and self.is_turn():
            self.game.table[self.player_number] = self.hand.pop(card)
            if self.f(self.game.table) == 4:
                print 'discarding'
                self.discard()
            else:
                self.changed()

    def is_turn(self):
        """Checks to see that it is the User's turn to play a card or bid."""
        # This ought to be re-implemented as a decorator
        return True if self.trick.turn == self.player_number else False

    def is_playable(self, card):
        """Checks that it is possible to play a given card, according to the 
           rules of the game."""
        leading_suit = self.trick.leading_suit
        if not leading_suit:
            self.trick.leading_suit = card[-1]
            return True
        hand = self.hand
        trump = self.trick.trump
        playables = filter(lambda x: x[-1] in [leading_suit, trump], hand)
        if not playables:
            return True
        elif card in playables:
            return True
        else:
            return False

    def changed(self):
        self.trick.turn = (self.trick.turn + 1) % 4
        self.trick.last_mod = time()

    def bidding_finished(self):
        self.trick.turn = self.trick.bidder
        self.trick.last_mod = time()

    def discard(self):
        number = lambda x,y: x if int(x[:-1]) > int(y[:-1]) else y
        suit = lambda suit:lambda x: True if x[-1] == suit else False
        leading_suit = self.trick.leading_suit
        table = list(self.game.table)
        try:
            winner = table.index(reduce(number, filter(suit(self.trump), table)))
        except TypeError:
            winner = table.index(reduce(number, filter(suit(leading_suit), table)))
        if winner in [0,2]:
            self.trick.team1.append(table)
        else:
            self.trick.team2.append(table)
        self.game.table = [None] * 4
        if not self.f(self.hand):
            self.next_trick()
        else:
            self.trick.turn = winner
            self.trick.last_mod = time()

    def next_trick(self):
        pass

