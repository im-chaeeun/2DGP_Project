from pico2d import *
import game_framework

import game_world
from practice import net_practice, server_practice
from practice.net_practice import Net
from practice.player_prcatice import Player
from court import Court
from practice.scorebox import Scorebox
from practice.shuttlecock_practice import Shuttlecock_Practice
from mode import title_mode

PIXEL_PER_METER = (10.0/0.3)    # 10pixel 30cm

# 공 칠 때 의 속도
RECEIVE_SPEED_KMPH = 25.0 # Km / Hour
RECEIVE_SPEED_MPM = (RECEIVE_SPEED_KMPH * 1000.0 / 60.0)
RECEIVE_SPEED_MPS = (RECEIVE_SPEED_MPM / 60.0)
RECEIVE_SPEED_PPS = (RECEIVE_SPEED_MPS * PIXEL_PER_METER)

# 네트와 충돌할 때 셔틀콕
NET_SPEED_KMPH = 5.0 # Km / Hour
NET_SPEED_MPM = (NET_SPEED_KMPH * 1000.0 / 60.0)
NET_SPEED_MPS = (NET_SPEED_MPM / 60.0)
NET_SPEED_PPS = (NET_SPEED_MPS * PIXEL_PER_METER)

GRAVITY_SPEED_MPS = 9.8
GRAVITY_SPEED_PPS = GRAVITY_SPEED_MPS * PIXEL_PER_METER

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            # game_framework.quit()
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # game_framework.quit()
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)

def init():
    global player
    global scorebox
    global shuttlecock
    global net
    global font
    global set_num

    running = True

    court = Court()
    game_world.add_object(court, 0)

    player = Player()
    game_world.add_object(player, 1)
    game_world.add_collision_pair('player1:shuttlecock', player, None)


    shuttlecock = Shuttlecock_Practice()
    game_world.add_object(shuttlecock, 2)
    game_world.add_collision_pair('player1:shuttlecock', None, shuttlecock)
    game_world.add_collision_pair('player2:shuttlecock', None, shuttlecock)
    game_world.add_collision_pair('net:shuttlecock', None, shuttlecock)

    scorebox = Scorebox()
    game_world.add_object(scorebox, 3)
    font = load_font('resource/ENCR10B.TTF', 40)

    net = Net()
    game_world.add_object(net, 1)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    shuttlecock.y = max(shuttlecock.y, 100)
    if game_world.collide(shuttlecock, player):
        print('플레이어 라켓과 셔틀콕 충돌')
        shuttlecock.is_flying = True
        shuttlecock.speed_y = RECEIVE_SPEED_PPS
        shuttlecock.dir = 1
        shuttlecock.update()


    if game_world.collide(shuttlecock, net):
        print('네트와 셔틀콕 충돌')
        shuttlecock.is_flying = True
        shuttlecock.speed_y = NET_SPEED_PPS
        shuttlecock.dir *= -1
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