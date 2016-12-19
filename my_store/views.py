import django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django_redis import get_redis_connection

from django_store.forms import ComplexityForm
from .models import *

redis = get_redis_connection("default")

@csrf_exempt
def login(request):
    return HttpResponse(loader.get_template('login.html').render())


@csrf_exempt
def index(request):
    context = {
        'entities': BoardGame.objects.all(),
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse("There is no such user")
        else:
            django.contrib.auth.login(request, user)
            context['user'] = user

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def product(request, id):
    template = loader.get_template('product.html')
    context = {
        'product': Product.objects.get(id=id)
    }
    return HttpResponse(template.render(context, request))


def board_game(request):
    template = loader.get_template('board_game.html')
    print("Cached complexity: " + str(redis.hget(request.user.username, 'complexity')))
    context = {
        'complexities': BoardGame.objects.values('complexity').distinct().order_by('complexity'),
        'playing_times': BoardGame.objects.values('playing_time').distinct().order_by('playing_time'),
        'cached_compl': [float(num) for num in redis.hget(request.user.username, 'complexity').decode('utf-8').replace('[','').replace(']', '').split(',')] if redis.hget(request.user.username, 'complexity') is not None else None,
        'cached_playing': [int(time) for time in redis.hget(request.user.username, 'playing_time').decode('utf-8').replace('[','').replace(']', '').split(',')] if redis.hget(request.user.username, 'playing_time') is not None else None,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def product_grid(request):
    compl_values = request.POST.getlist('complexity[]')
    playing_time_values = request.POST.getlist('playing_time[]')
    games = BoardGame.objects.all()
    user_cache = {}
    if compl_values:
        games = games.filter(complexity__in=compl_values)
        user_cache['complexity'] = [float(i) for i in compl_values]
    if playing_time_values:
        games = games.filter(playing_time__in=playing_time_values)
        user_cache['playing_time'] = [int(i) for i in playing_time_values]
    context = {
        'entities': games
    }
    if len(user_cache) != 0:
        redis.hmset(request.user.username, user_cache)
        print(redis.hgetall(request.user.username))
    return render_to_response('product_grid.html', context)

