from pico2d import load_image, load_font, draw_rectangle

from competition.player1_competition import Player1
from competition.player2_competition import Player2


class Net:
    def __init__(self):
        self.x = 400
        self.y = 50

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass
    def get_bb(self):
        return self.x - 5, self.y, self.x + 10, self.y + 220