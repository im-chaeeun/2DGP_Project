from pico2d import *
import game_framework

import game_world
from competition.net import Net
from competition.player1_competition import Player1
from competition.player2_competition import Player2
from court import Court
from competition.scorebox import Scorebox
from competition.shuttlecock_competition import Shuttlecock

PIXEL_PER_METER = (10.0/0.3)    # 10pixel 30cm
RUN_SPEED_KMPH = 25.0   # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0  # 분당 몇 m?
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0    # 초당 몇 m?
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

GRAVITY_SPEED_MPS = 9.8
GRAVITY_SPEED_PPS = GRAVITY_SPEED_MPS * PIXEL_PER_METER

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
    global player1, player2
    global scorebox
    global shuttlecock

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player1 = Player1()
    game_world.add_object(player1, 1)
    game_world.add_collision_pair('player1:shuttlecock', player1, None)

    player2 = Player2()
    game_world.add_object(player2, 1)
    game_world.add_collision_pair('player2:shuttlecock', player1, None)

    shuttlecock = Shuttlecock()
    game_world.add_object(shuttlecock, 2)
    game_world.add_collision_pair('player1:shuttlecock', None, shuttlecock)
    game_world.add_collision_pair('player2:shuttlecock', None, shuttlecock)
    game_world.add_collision_pair('net:shuttlecock', None, shuttlecock)

    scorebox = Scorebox()
    game_world.add_object(scorebox, 3)

    net = Net()
    game_world.add_object(net, 1)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()

    if game_world.collide(shuttlecock, player1):
        print('플레이어1 라켓과 셔틀콕 충돌')
        shuttlecock.is_flying = True
        shuttlecock.speed_y = RUN_SPEED_PPS
        shuttlecock.dir = 1
        shuttlecock.update()

    if game_world.collide(shuttlecock, player2):
        print('플레이어2 라켓과 셔틀콕 충돌')
        shuttlecock.is_flying = True
        shuttlecock.speed_y = RUN_SPEED_PPS
        shuttlecock.dir = -1
        shuttlecock.update()

    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass