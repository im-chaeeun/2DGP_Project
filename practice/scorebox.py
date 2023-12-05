from pico2d import load_image, load_font

from competition import server_competition
from competition.player1_competition import Player1
from competition.player2_competition import Player2
from competition.shuttlecock_competition import Shuttlecock


class Scorebox:
    def __init__(self):
        self.image = load_image('resource/scorebox.png')

    def draw(self):
        self.image.draw(400, 570)

    def update(self):
        pass