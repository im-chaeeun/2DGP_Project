from pico2d import *
import game_framework

import game_world
from player_prcatice import Player
from court import Court
from shuttlecock_practice import Shuttlecock_Practice


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global grass
    global player
    global scorebox
    global shuttlecock_practice

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player = Player()
    game_world.add_object(player, 1)

    shuttlecock_practice = Shuttlecock_Practice()
    game_world.add_object(shuttlecock_practice, 2)



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # fill here
    # game_world.handle_collisions()

    if game_world.collide(shuttlecock_practice, player):
        print('플레이어 라켓과 셔틀콕 충돌')
        shuttlecock_practice.is_flying = True
        shuttlecock_practice.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass