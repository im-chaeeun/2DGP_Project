from pico2d import *
import game_framework

import game_world
from player_prcatice import Player
from court import Court
from practice_machine import Practice_Machine
from shuttlecock_practice import Shuttlecock_Practice
from arrow_practice_mode import Arrow
#from stamina_bar import Stamina

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
            player.handle_event(event)

def init():
    global player
    global shuttlecock_practice
    global prctice_machine
    global stamina
    #global arrow

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player = Player()
    game_world.add_object(player, 1)

    shuttlecock_practice = Shuttlecock_Practice()
    game_world.add_object(shuttlecock_practice, 2)

    # practice_machine = Practice_Machine()
    # game_world.add_object(practice_machine, 2)
    # Practice_Machine 클래스의 인스턴스 생성
    practice_machine_instance = Practice_Machine()
    # game_world에 객체 추가
    game_world.add_object(practice_machine_instance, 2)

    #stamina = Stamina()
    #game_world.add_object(stamina, 3)

    #arrow = Arrow()
    #game_world.add_object(arrow, 3)


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
        shuttlecock_practice.speed_y = RUN_SPEED_PPS
        shuttlecock_practice.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass