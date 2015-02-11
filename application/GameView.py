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
        self.m_played = '{} played {}\n'
        self.m_won = '{} won with {}\n'

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
            'bids': list(self.bids),
            'message':self.game.message
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
        player_number = self.player_number
        dealer = self.game.dealer
        dealer_bid_4 = player_number == dealer and bid == 4
        dealer_force_bid = player_number == dealer and max(self.bids) == 1
        if self.is_turn():
            self.game.message = ''
            if bid <= max(self.bids) and not dealer_bid_4:
                if dealer_force_bid and bid == 0:
                    bid = 2
                else:
                    bid = 0
            self.bids[player_number] = bid
            if 1 not in self.bids:
                self.trick.bid = max(self.bids)
                if dealer_bid_4:
                    self.trick.bidder = dealer
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
            self.game.message = ''
            if self.f(self.game.table) == 4:
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
        hand = filter(None, self.hand)
        trump = self.trick.trump
        follow = [x for x in hand if x[-1] == leading_suit]
        playables = follow + [x for x in hand if x[-1] == trump]
        if not follow or (card in playables):
            return True
        else:
            return False

    def changed(self):
        self.trick.turn = (self.trick.turn + 1) % 4
        self.trick.last_mod = int(time())

    def bidding_finished(self):
        self.trick.turn = self.trick.bidder
        self.trick.last_mod = int(time())

    def discard(self):
        number = lambda x,y: x if int(x[:-1]) > int(y[:-1]) else y
        suit = lambda suit:lambda x: True if x[-1] == suit else False
        leading_suit = self.trick.leading_suit
        table = list(self.game.table)
        try:
            winner = table.index(reduce(number, filter(suit(self.trick.trump), table)))
        except TypeError:
            winner = table.index(reduce(number, filter(suit(leading_suit), table)))
        if winner in [0,2]:
            self.trick.team1.append(table)
        else:
            self.trick.team2.append(table)
        status = ''
        for i in range(4):
            player_number = (self.trick.turn + i) % 4
            if player_number == winner:
                status += self.m_won.format(self.game.players[player_number].username, 
                                            self.game.table[player_number])
            else:
                status += self.m_played.format(self.game.players[player_number].username, 
                                               self.game.table[player_number])
        self.game.message = status
        print status
        self.game.table[0] = None
        self.game.table[1] = None
        self.game.table[2] = None
        self.game.table[3] = None
        self.trick.leading_suit = None
        if not self.f(self.hand):
            self.next_trick()
        else:
            self.trick.turn = winner
            self.trick.last_mod = int(time())
            self.trick.leading_suit = None

    def next_trick(self):
        trump = self.trick.trump
        bidder = 1 if self.trick.bidder in [0,2] else 2
        bid = max(self.bids)
        score1 = 0
        score2 = 0
        team1 = [card for group in self.game.trick.team1 for card in list(group)]
        team2 = [card for group in self.game.trick.team2 for card in list(group)]
        trump_cards = [card for card in team1+team2 if card[-1] == trump]
        high = max(trump_cards, key=lambda x:int(x[:-1]))
        low = min(trump_cards, key=lambda x:int(x[:-1]))
        jack = '11'+trump
        game_count = lambda x: 10 if x[1] == '0' else int(card[1])
        team1_game = sum([game_count(card) for card in team1 if len(card)>2])
        team2_game = sum([game_count(card) for card in team2 if len(card)>2])
        message = '\nTrick Finished!\n\n'
        if high in team1:
            score1 += 1
            message += 'Team 1 got the high card: {}\n'.format(high)
        elif high in team2:
            score2 += 1
            message += 'Team 2 got the high card: {}\n'.format(high)
        if low in team1:
            score1 += 1
            message += 'Team 1 got the low card: {}\n'.format(low)
        elif low in team2:
            score2 += 1
            message += 'Team 2 got the low card: {}\n'.format(low)
        if jack in team1:
            score1 += 1
            message += 'Team 1 got the jack\n'
        elif jack in team2:
            score2 += 1
            message += 'Team 2 got the jack\n'
        if team1_game > team2_game:
            score1 += 1
            message += 'Team 1 got game\n'
        elif team2_game > team1_game:
            score2 += 1
            message += 'Team 2 got game\n'
        message += 'Team 1 game: {}\n'.format(team1_game)
        message += 'Team 2 game: {}\n'.format(team2_game)
        print message
        self.game.message += message

        if bidder == 1 and score1 < bid:
            score1 = -bid
            message += 'Team 1 did not make their {} bid'.format(bid)
        elif bidder == 2 and score2 < bid:
            score2 = -bid
            message += 'Team 2 did not make their {} bid'.format(bid)
        self.game.team1_score += score1
        self.game.team2_score += score2
        
        self.game.dealer = (self.game.dealer + 1) % 4
        if not self.finished(score1, score2):
            self.game.deal()

    def finished(self, score1, score2):
        play_to = self.game.play_to
        team1 = score1 >= play_to and (score1 - score2) >= 2
        team2 = score2 >= play_to and (score2 - score1) >= 2
        return team1 or team2
        

        

