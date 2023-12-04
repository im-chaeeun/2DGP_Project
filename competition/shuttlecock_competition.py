from pico2d import *
import game_framework
import game_world
from competition import server_competition

PIXEL_PER_METER = (10.0/0.3)    # 10pixel 30cm
RUN_SPEED_KMPH = 20.0   # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0  # 분당 몇 m?
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0    # 초당 몇 m?
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER



GRAVITY_SPEED_MPS = 9.8
GRAVITY_SPEED_PPS = GRAVITY_SPEED_MPS * PIXEL_PER_METER


class Shuttlecock:
    image = None
    def __init__(self):
        self.image = load_image('resource/shuttlecock.png')
        self.x, self.y = 260, 265

        self.time = 0
        self.is_flying = False
        self.state = 'Idle'
        self.start_time = get_time()
        self.speed_y = 0
        self.dir = 0
        self.who_hit_shuttlecock = None
        self.who_get_score = 'player1'
        self.player1_score, self.player2_score = 0, 0
        self.remove_wait_time = 0
    def draw(self):
        # 코트 왼쪽에 있을 때 셔틀콕 그리기
        if self.x <= 200:
            self.image.clip_composite_draw(0, 0, 7, 8, -130, ' ', self.x, self.y, 28, 32)
        elif self.x > 200 and self.x <= 400:
            self.image.clip_composite_draw(0, 0, 7, 8, -80, ' ', self.x, self.y, 28, 32)
        # 코트 오른쪽에 있을 때 셔틀콕 그리기
        if self.x > 400 and self.x <= 600:
            self.image.clip_composite_draw(0, 0, 7, 8, 130, ' ', self.x, self.y, 28, 32)
        elif self.x > 600 and self.x:
             self.image.clip_composite_draw(0, 0, 7, 8, 90, ' ', self.x, self.y, 28, 32)
        draw_rectangle(*self.get_bb())

    def update(self):

        if self.is_flying:
            self.time += 0.1
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time  # 방향 나중에 곱해라
            self.y += self.speed_y * game_framework.frame_time
            if get_time() - self.start_time > 0.6:
                self.start_time = get_time()
                self.speed_y -= RUN_SPEED_PPS

            #Shuttlecock이 땅보다 아래로 떨어지지 않도록 제한

            self.y = max(self.y, 100)
            # Shuttlecock이 땅에 닿았는지 확인
            if self.y == 100:
                self.is_flying = False
                self.time = 0
                self.check_who_get_score()



    def get_bb(self):
        return self.x - 14, self.y - 16, self.x + 14, self.y + 16

    def handle_event(self, event):
        # Shuttlecock 이벤트 처리 추가
        pass

    def handle_collision(self, group, other):
        pass

    def check_who_get_score(self):
        if server_competition.who_hit_shuttlecock == 'player1':
            if self.x > 700 or self.x < 400:
                server_competition.who_get_score = 'player2'
                print('플레이어2 승')
                server_competition.player2_score += 1
                server_competition.who_get_score = 'player2'
            else:
                server_competition.who_hit_shuttlecock = 'player1'
                print('플레이어1 승')
                server_competition.player1_score += 1
                server_competition.who_get_score = 'player1'
        elif server_competition.who_hit_shuttlecock == 'player2':
            if self.x < 100 or self.x > 400:
                server_competition.who_get_score = 'player1'
                print('플레이어1 승')
                server_competition.player1_score += 1
                server_competition.who_get_score = 'player1'
            else:
                server_competition.who_hit_shuttlecock = 'player2'
                print('플레이어2 승')
                server_competition.player2_score += 1
                server_competition.who_get_score = 'player2'

        game_world.remove_object(self)
        #  셔틀콕과 플레이어 위치 초기화
        if server_competition.who_get_score == 'player1':
            self.x, self.y = 260, 265
        elif server_competition.who_get_score == 'player2':
            self.x, self.y = 540, 265
        game_world.add_object(self, 2)
        game_world.add_collision_pair('player1:shuttlecock', None, self)
        game_world.add_collision_pair('player2:shuttlecock', None, self)
        game_world.add_collision_pair('net:shuttlecock', None, self)






