from pico2d import *

import game_world
from court import Court
from player1 import Player1


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player1.handle_event(event)


def reset_world():
    global running
    global court
    global world
    global player1

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player1 = Player1()
    game_world.add_object(player1, 1)

    # ball = Ball()
    # game_world.add_object(ball, 1)



def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
reset_world()


# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()