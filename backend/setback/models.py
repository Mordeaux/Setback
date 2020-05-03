from random import shuffle

from django.db import models
from django.contrib.auth.models import User
from django.core.serializers import serialize


class Player(models.Model):
    """"""
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    display_name = models.CharField(max_length=30)


class Card(models.Model):
    """"""
    class Suit(models.IntegerChoices):
        HEARTS = 0
        DIAMONDS = 1
        CLUBS = 2
        SPADES = 3
    class Rank(models.IntegerChoices):
        TWO = 0
        THREE = 1
        FOUR = 2
        FIVE = 3
        SIX = 4
        SEVEN = 5
        EIGHT = 6
        NINE = 7
        TEN = 8
        JACK = 9
        QUEEN = 10
        KING = 11
        ACE = 12
    suit = models.IntegerField(choices=Suit.choices)
    rank = models.IntegerField(choices=Rank.choices)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.get_rank_display()} of {self.get_suit_display()}'


class MatchPlayerGame(models.Model):
    """"""
    class Position(models.IntegerChoices):
        FIRST = 0
        SECOND = 1
        THIRD = 2
        FOURTH = 3
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
    )
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
    )
    position = models.IntegerField(choices=Position.choices)
    hand = models.ManyToManyField(Card, related_name='+')
    currently_played = models.ForeignKey(
        Card,
        on_delete=models.DO_NOTHING,
        related_name='+',
        blank=True,
        null=True,
    )


class Deck(models.Model):
    """"""
    position = models.IntegerField()
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='+'
    )


class GameManager(models.Manager):
    def new_game(self, players):
        game = self.create(
            team_one_score=0,
            team_two_score=0,
        )
        game.add_players(players)
        game.shuffle()
        game.save()
        return game


class Game(models.Model):
    """"""
    players = models.ManyToManyField(
        Player,
        through='MatchPlayerGame',
    )
    team_one_score = models.IntegerField()
    team_two_score = models.IntegerField()
    next_to_play = models.ForeignKey(
        'MatchPlayerGame',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    deck = models.ManyToManyField(
        Card,
        through=Deck,
    )

    objects = GameManager()

    def add_players(self, players):
        for index, player in enumerate(players):
            match_player_game = MatchPlayerGame.objects.create(
                position=index,
                game=self,
                player=player,
            )
            if index == 0:
                self.next_to_play = match_player_game

    def shuffle(self):
        self.deck.clear()
        cards = list(Card.objects.all())
        shuffle(cards)
        for index, card in enumerate(cards):
            deck = Deck.objects.create(
                position=index,
                game=self,
                card=card,
            )

    def deal(self):
        deck = self.deck.all()
        for match_player_game in self.matchplayergame_set.all():
            hand = deck[0:6]
            match_player_game.hand.set(hand)
            self.deck.remove(*hand)

    def player_view(self, player):
        hands = {}
        for mpg in self.matchplayergame_set.all():
            hands[mpg.player.display_name] = []
            for card in mpg.hand.all():
                if mpg.player == player:
                    hands[mpg.player.display_name].append(
                        {
                            'id': card.id,
                            'rank': card.rank,
                            'suit': card.suit,
                        }
                    )
                else:
                    hands[mpg.player.display_name].append({})
        return hands
