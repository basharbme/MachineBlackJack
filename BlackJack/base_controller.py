import json
import os
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.template import loader
from BlackJack.AI.probability import advice, generate_game_id
from BlackJack.AI.game import Game
from BlackJack.AI.card import Card
from BlackJack.settings import BASE_DIR

def index(request):
    index_page = loader.get_template('index.html')
    return  HttpResponse(index_page.render())

def start_game(request):
    request.session['game_id'] = generate_game_id()
    game = Game()
    game.next_round()
    game_json = game.to_json()
    with open(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'], "w") as file:
        file.write(game_json)
    return HttpResponse(game_json)

def hit(request):
    game_json = ''
    with open(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'], "r") as file:
        game_json = file.read()
    game_json = json.loads(game_json)
    game = Game(deck=game_json['deck'], 
    state={'dealer': game_json['dealer'], 'self': game_json['self']}, 
    chain=game_json['chain'])
    game_json = {}
    if game.next_round('1'):
        print(game.chain)
        game_json['result'] = game.finish_game()
        game.learn(game_json['result'])
        game_json['game'] = game.to_json()
        with open(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'], "w") as file:
            file.write(game_json['game'])
        game_json = json.dumps(game_json)
        os.remove(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'])

    else:
        game_json = game.to_json()
        with open(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'], "w") as file:
            file.write(game_json)
    return HttpResponse(game_json)
    

def get_rec(request):
    with open(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'], "r") as file:
        game = json.loads(file.read())
    deck = []
    for prop in game['deck']:
        deck.append(json.loads(prop))
    return HttpResponse(json.dumps(advice(deck, 
    Card.count_value(game['dealer']), 
    Card.count_value(game['self']))))

def stay(request):

    game_json = ''

    with open(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'], "r") as file:
        game_json = file.read()
    
    game_json = json.loads(game_json)
    game = Game(deck=game_json['deck'], 
    state={'dealer': game_json['dealer'], 'self': game_json['self']}, 
    chain=game_json['chain'])
    game_json['result'] = game.finish_game()
    game.learn(game_json['result'])
    game_json['game'] = game.to_json()
    game_json = json.dumps(game_json)
    os.remove(BASE_DIR+'/BlackJack/Game/games/'+request.session['game_id'])
    
    return HttpResponse(game_json)
