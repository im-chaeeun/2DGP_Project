import random

from pico2d import *
import game_framework
import game_world
from competition import server_competition
from practice import server_practice

PIXEL_PER_METER = (10.0/0.3)    # 10pixel 30cm
RUN_SPEED_KMPH = 20.0   # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0  # 분당 몇 m?
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0    # 초당 몇 m?
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER


# 공 칠 때 의 속도
RECEIVE_SPEED_KMPH = 20.0 # Km / Hour
RECEIVE_SPEED_MPM = (RECEIVE_SPEED_KMPH * 1000.0 / 60.0)
RECEIVE_SPEED_MPS = (RECEIVE_SPEED_MPM / 60.0)
RECEIVE_SPEED_PPS = (RECEIVE_SPEED_MPS * PIXEL_PER_METER)
# 파워게이지 다 찼을 때 의 속도
POWER_SPEED_KMPH = 70.0 # Km / Hour
POWER_SPEED_MPM = (POWER_SPEED_KMPH * 1000.0 / 60.0)
POWER_SPEED_MPS = (POWER_SPEED_MPM / 60.0)
POWER_SPEED_PPS = (POWER_SPEED_MPS * PIXEL_PER_METER)


GRAVITY_SPEED_MPS = 9.8
GRAVITY_SPEED_PPS = GRAVITY_SPEED_MPS * PIXEL_PER_METER
class Shuttlecock_Practice:
    image = None
    def __init__(self):
        self.image = load_image('resource/shuttlecock.png')
        self.x, self.y = 600, 500

        self.time = 0
        self.is_flying = True
        self.state = 'Idle'
        self.start_time = get_time()
        self.speed_y = 0
        self.dir = -1
        self.is_removed = False  # 객체가 삭제되었는지 여부를 나타내는 변수


    def draw(self):
        if self.y <= 300 and self.x <= 400:
            self.image.clip_composite_draw(0, 0, 7, 8, -130, ' ', self.x, self.y, 28, 32)
        elif self.y > 300 and self.x <= 400:
            self.image.clip_composite_draw(0, 0, 7, 8, -50, ' ', self.x, self.y, 28, 32)
        # 코트 오른쪽에 있을 때 셔틀콕 그리기
        if self.y <= 300 and self.x > 400:
            self.image.clip_composite_draw(0, 0, 7, 8, 130, ' ', self.x, self.y, 28, 32)
        elif self.y > 300 and self.x > 400:
             self.image.clip_composite_draw(0, 0, 7, 8, 50, ' ', self.x, self.y, 28, 32)
        # draw_rectangle(*self.get_bb())

    def update(self):

        if self.is_flying:
            self.time += 0.1
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time  # 방향 나중에 곱해라
            self.y += self.speed_y * game_framework.frame_time
            if server_practice.player_powergage >= 630:
                if get_time() - self.start_time > 0.4:
                   self.start_time = get_time()
                   self.speed_y -= POWER_SPEED_PPS
                   server_practice.player_powergage = 0
            elif server_practice.player_powergage < 630:
                if get_time() - self.start_time > 0.6:
                   self.start_time = get_time()
                   self.speed_y -= RECEIVE_SPEED_PPS



            #Shuttlecock이 땅보다 아래로 떨어지지 않도록 제한
            self.y = max(self.y, 100)
            # Shuttlecock이 땅에 닿았는지 확인
            if self.y == 100:
                self.is_flying = False
                self.time = 0
                self.speed_y = 0
                self.dir = -1
                #  셔틀콕 위치 초기화
                self.x, self.y = random.randint(450, 500), random.randint(400, 600)
                self.is_flying = True

                game_world.add_object(self, 2)
                game_world.add_collision_pair('player1:shuttlecock', None, self)
                game_world.add_collision_pair('net:shuttlecock', None, self)

                game_world.remove_object(self)
    def get_bb(self):
        return self.x - 14, self.y - 16, self.x + 14, self.y + 16

    def handle_event(self, event):
        # Shuttlecock 이벤트 처리 추가
        pass

    def handle_collision(self, group, other):
        pass






