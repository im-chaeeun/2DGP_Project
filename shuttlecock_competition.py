from pico2d import *
import math
import game_framework
import game_world
import player1_competition


class Shuttlecock:
    image = None

    def __init__(self):
        if Shuttlecock.image is None:
            Shuttlecock.image = load_image('shuttlecock.png')
        self.x, self.y, self.velocity = 260, 265, 2
        self.angle = math.radians(45)  # 초기 각도 설정
        self.gravity = 9.8  # 중력 가속도
        self.time = 0
        self.is_flying = False

    def draw(self):
        self.image.clip_draw(0, 0, 7, 8, self.x, self.y, 28, 32)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.is_flying:
            self.time += 0.1
            self.x = self.x + self.velocity * math.cos(self.angle) * self.time
            self.y = self.y + self.velocity * math.sin(self.angle) * self.time - 0.5 * self.gravity * self.time ** 2 * 0.5

            # Shuttlecock이 땅보다 아래로 떨어지지 않도록 제한
            self.y = max(self.y, 70)

            # Shuttlecock이 땅에 닿았는지 확인
            if self.y == 70:
                self.is_flying = False
                self.time = 0

    def get_bb(self):
        return self.x - 14, self.y - 16, self.x + 14, self.y + 16

    def handle_event(self, event):
        # Shuttlecock 이벤트 처리 추가
        pass