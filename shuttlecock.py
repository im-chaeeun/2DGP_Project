from pico2d import *
import game_world

class Shuttlecock:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 0):
        if Shuttlecock.image == None:
            Shuttlecock.image = load_image('shuttlecock.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.clip_draw(0, 0, 7, 8, self.x, self.y, 28, 32)

    def update(self):
        self.x += self.velocity

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)