from pico2d import load_image, load_font

from competition.player1_competition import Player1
from competition.player2_competition import Player2


class Scorebox:
    def __init__(self):
        self.image = load_image('resource/scorebox.png')
        self.font = load_font('resource/ENCR10B.TTF', 40)

    def draw(self):
        player1_instance = Player1()
        player2_instance = Player2()

        self.image.draw(400, 570)
        self.font.draw(333, 575,   f'{player1_instance.score}', (255, 255, 255))
        self.font.draw(441, 575, f'{player2_instance.score}', (255, 255, 255))

    def update(self):
        pass