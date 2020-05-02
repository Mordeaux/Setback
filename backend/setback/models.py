from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    """"""
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    display_name = models.CharField(max_length=30)


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
    )


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
        Game,
        on_delete=models.CASCADE,
    )
    position = models.IntegerField(choices=Position.choices)
    cards = models.ManyToManyField(Card, related_name='+')
    currently_played = models.ForeignKey(
        Card,
        on_delete=models.DO_NOTHING,
        related_name='+',
    )
