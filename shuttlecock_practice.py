from pico2d import *
import game_framework
import game_world
import player1_competition

PIXEL_PER_METER = (10.0/0.3)    # 10pixel 30cm
RUN_SPEED_KMPH = 20.0   # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0  # 분당 몇 m?
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0    # 초당 몇 m?
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

GRAVITY_SPEED_MPS = 9.8
GRAVITY_SPEED_PPS = GRAVITY_SPEED_MPS * PIXEL_PER_METER


class Shuttlecock_Practice:
    image = None

    def __init__(self):
        if Shuttlecock_Practice.image is None:
            Shuttlecock_Practice.image = load_image('shuttlecock.png')
        self.x, self.y, self.velocity = 630, 180, 2
        self.time = 0
        self.state = 'Idle'
        self.start_time = get_time()
        self.speed_y = 0

    def draw(self):
        self.image.clip_draw(0, 0, 7, 8, self.x, self.y, 28, 32)
        draw_rectangle(*self.get_bb())

    def update(self):

        if get_time() - self.start_time > 0.05:  # 3초마다
            self.start_time = get_time()
            self.speed_y = RUN_SPEED_PPS  # 초기 속도 설정


        self.time += 0.1
        self.x -= RUN_SPEED_PPS * game_framework.frame_time  # 왼쪽으로 이동
        self.y += self.speed_y * game_framework.frame_time

        # Shuttlecock이 땅보다 아래로 떨어지지 않도록 제한
        self.y = max(self.y, 100)
        # Shuttlecock이 땅에 닿았는지 확인
        if self.y == 100:
            self.time = 0

    def get_bb(self):
        return self.x - 14, self.y - 16, self.x + 14, self.y + 16

    def handle_event(self, event):
        # Shuttlecock 이벤트 처리 추가
        pass