from pico2d import *

import game_framework
import game_world

class Shuttlecock:
    image = None

    def __init__(self, x=250, y=300, velocity=2):
        if Shuttlecock.image is None:
            Shuttlecock.image = load_image('shuttlecock.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.racket_x = 0  # 라켓의 초기 x 위치
        self.racket_y = 0  # 라켓의 초기 y 위치
        self.racket_speed = 50  # 라켓의 이동 속도

    def draw(self):
        self.image.clip_draw(0, 0, 7, 8, self.x + self.racket_x, self.y + self.racket_y, 28, 32)

    def update(self):
        self.x += self.velocity

        # 라켓 위치 업데이트
        self.racket_x += self.racket_speed * game_framework.frame_time
        self.racket_y += self.racket_speed * game_framework.frame_time

    def handle_event(self, event):
        # Shuttlecock 이벤트 처리 추가
        pass