from django.shortcuts import render
from django.http import JsonResponse
from .models import (
    Player,
    Game,
)

# Create your views here.
def index(request):
    players = []
    for i in range(4):
        player, _ = Player.objects.get_or_create(
            display_name=f'Player ${i}',
        )
        players.append(player)
#   game = Game.objects.new_game(players)

    game = Game.objects.get(pk=4)
    game.shuffle()
    game.deal()

    return JsonResponse({
        'data': game.player_view(Player.objects.get(pk=2)),
    })
