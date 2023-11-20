from pico2d import load_image, load_font

from object.player1 import Player1
from object.player2 import Player2


class Scorebox:
    def __init__(self):
        self.image = load_image('scorebox.png')
        self.font = load_font('ENCR10B.TTF', 40)

    def draw(self):
        player1_instance = Player1()
        player2_instance = Player2()

        self.image.draw(400, 570)
        self.font.draw(333, 575,   f'{player1_instance.score}', (255, 255, 0))
        self.font.draw(441, 575, f'{player2_instance.score}', (255, 255, 0))

    def update(self):
        pass