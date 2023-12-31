from pico2d import *
import game_framework

import game_world
from competition import net, server_competition
from competition.net import Net
from competition.notice_set_num import Notice_Set_Num
from competition.player1_competition import Player1
from competition.player2_competition import Player2
from court import Court
from competition.scorebox import Scorebox
from competition.shuttlecock_competition import Shuttlecock
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

# 파워게이지 다 찼을 때 의 속도
POWER_SPEED_KMPH = 35.0 # Km / Hour
POWER_SPEED_MPM = (POWER_SPEED_KMPH * 1000.0 / 60.0)
POWER_SPEED_MPS = (POWER_SPEED_MPM / 60.0)
POWER_SPEED_PPS = (POWER_SPEED_MPS * PIXEL_PER_METER)


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
            player1.handle_event(event)
            player2.handle_event(event)

def init():
    global player1, player2
    global scorebox
    global shuttlecock
    global net
    global font
    global set_num
    global racket_hit_sound

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


    racket_hit_sound = load_wav('resource/sound_attack.wav')
    racket_hit_sound.set_volume(60)

    scorebox = Scorebox()
    game_world.add_object(scorebox, 3)
    font = load_font('resource/ENCR10B.TTF', 40)

    net = Net()
    game_world.add_object(net, 1)

    set_num = Notice_Set_Num()
    game_world.add_object(set_num, 3)
def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    shuttlecock.y = max(shuttlecock.y, 100)
    server_competition.player1_powergage = clamp(0, server_competition.player1_powergage, 640)
    server_competition.player2_powergage = clamp(0, server_competition.player2_powergage, 640)

    if game_world.collide(shuttlecock, player1):
        print('플레이어1 라켓과 셔틀콕 충돌')
        racket_hit_sound.play()
        server_competition.player1_powergage += 200
        shuttlecock.is_flying = True
        server_competition.who_hit_shuttlecock = 'player1'
        if server_competition.player1_powergage >= 640:
            shuttlecock.speed_y = POWER_SPEED_PPS
            server_competition.player1_powergage = 0
        else:
            shuttlecock.speed_y = RECEIVE_SPEED_PPS
        shuttlecock.dir = 1
        shuttlecock.update()

    if game_world.collide(shuttlecock, player2):
        print('플레이어2 라켓과 셔틀콕 충돌')
        racket_hit_sound.play()
        server_competition.player2_powergage += 200
        shuttlecock.is_flying = True
        server_competition.who_hit_shuttlecock = 'player2'
        if server_competition.player2_powergage >= 640:
            shuttlecock.speed_y = POWER_SPEED_PPS
            server_competition.player2_powergage = 0
        else:
            shuttlecock.speed_y = RECEIVE_SPEED_PPS
        shuttlecock.dir = -1
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