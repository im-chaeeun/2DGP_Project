from pico2d import *

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
    world = []

    court = Court()
    world.append(court)

    player1 = Player1()
    world.append(player1)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
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