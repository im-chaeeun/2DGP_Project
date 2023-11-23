from pico2d import *

import game_framework
import game_world

class Shuttlecock:
    image = None

    def __init__(self, x = 260, y = 250, velocity = 2, angle = 45):
        if Shuttlecock.image is None:
            Shuttlecock.image = load_image('shuttlecock.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.angle = angle
        self.gravity = 9.8  # 중력 가속도
        self.time = 0
        self.is_flying = False

    def draw(self):
        self.image.clip_draw(0, 0, 7, 8, self.x, self.y, 28, 32)
        # if self.is_flying:
        #     self.image.clip_draw(0, 0, 7, 8, self.x + self.racket_x, self.y + self.racket_y, 28, 32)
        #     # draw_rectangle(self.x - 5, self.y - 5, self.x + 5, self.y + 5)
        # else:
        #     draw_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y + 10)

    def update(self):
        if self.is_flying:
            self.time += 0.1
            self.x = self.x + self.velocity * math.cos(self.angle) * self.time
            self.y = self.y + self.velocity * math.sin(self.angle) * self.time - 0.5 * self.gravity * self.time ** 2
            if self.y < 0:
                self.is_flying = False
                self.time = 0
        pass

    def hit(self, racket_x, racket_y):
        if not self.is_flying:
            self.is_flying = True
            self.x, self.y = racket_x, racket_y
            self.angle = math.radians(45)  # 45도 각도로 발사

    def handle_event(self, event):
        # Shuttlecock 이벤트 처리 추가
        pass