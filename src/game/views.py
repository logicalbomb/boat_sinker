from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .error import handle_create_error
from .models import Game


def index(request):
    latest_game_list = Game.objects.order_by("-pub_date")[:5]
    context = {"latest_game_list": latest_game_list}
    return render(request, "game/index.html", context)


def create(request):
    return render(request, 'game/create.html')


def add(request):
    try:
        sea_map = request.POST["sea_map"]
    except KeyError:
        return handle_create_error(request, "You didn't send a sea_map.")

    if not sea_map:
        return handle_create_error(request, "You sent an empty sea_map.")
    
    # TODO: validate sea_map and save a proper game

    game = Game.objects.create()
    game.sea_map = sea_map
    game.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user  hits the Back button.
    return HttpResponseRedirect(reverse("game:solution", args=(game.id,)))


def solution(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, "game/solution.html", {"game": game})
