from pico2d import load_image, load_font

from competition import server_competition
from competition.player1_competition import Player1
from competition.player2_competition import Player2
from competition.shuttlecock_competition import Shuttlecock


class Scorebox:
    def __init__(self):
        self.image = load_image('resource/scorebox.png')
        self.font = load_font('resource/ENCR10B.TTF', 40)

        self.score = Shuttlecock()

    def draw(self):
        self.image.draw(400, 570)

        self.font.draw(333, 575,   f'{server_competition.player1_score}', (255, 255, 255))
        self.font.draw(441, 575, f'{server_competition.player1_score}', (255, 255, 255))
        # print('플레이어 1',self.player1_instance.score)
        # print('플레이어 2', self.player2_instance.score)
    def update(self):
        # if Shuttlecock.who_get_score == 'player2':
        #     self.player2_instance.score += 1
        # elif Shuttlecock.who_get_score == 'player1':
        #     self.player1_instance.score += 1
        pass