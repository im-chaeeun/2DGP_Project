from pico2d import load_image, load_font

from competition import server_competition
from competition.player1_competition import Player1
from competition.player2_competition import Player2
from competition.shuttlecock_competition import Shuttlecock


class Scorebox:
    def __init__(self):
        self.image = load_image('resource/scorebox.png')
        self.font_score = load_font('resource/ENCR10B.TTF', 40)
        self.font_set_score = load_font('resource/ENCR10B.TTF', 20)
        self.score = Shuttlecock()

    def draw(self):
        self.image.draw(400, 570)

        # 현재 점수
        self.font_score.draw(333, 575,   f'{server_competition.player1_score}', (255, 255, 255))
        self.font_score.draw(441, 575, f'{server_competition.player2_score}', (255, 255, 255))
        # 세트 점수
        self.font_set_score.draw(380, 575, f'{server_competition.player1_set_score}', (255, 255, 255))
        self.font_set_score.draw(410, 575, f'{server_competition.player2_set_score}', (255, 255, 255))
    def update(self):
        pass