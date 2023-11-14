import random

from pico2d import *
import game_framework

import game_world
from player1 import Player1
from player2 import Player2
from court import Court
from ball import Ball


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player1.handle_event(event)
            player2.handle_event(event)

def init():
    global grass
    global player1, player2
    # global balls

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player1 = Player1()
    game_world.add_object(player1, 1)
    player2 = Player2()
    game_world.add_object(player2, 1)



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # fill here
    # game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass