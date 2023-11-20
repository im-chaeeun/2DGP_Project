from pico2d import *

import game_framework
import game_world

class Shuttlecock:
    image = None

    def __init__(self, x = 250, y = 300, velocity = 2):
        if Shuttlecock.image == None:
            Shuttlecock.image = load_image('shuttlecock.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.clip_draw(0, 0, 7, 8, self.x, self.y, 28, 32)

    def update(self):
        self.x += self.velocity

    def handle_event(self, event):
        # Shuttlecock 이벤트 처리 추가
        pass