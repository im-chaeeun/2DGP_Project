from pico2d import load_image, load_font

import game_world
from competition import server_competition
from competition.player1_competition import Player1
from competition.player2_competition import Player2
from competition.shuttlecock_competition import Shuttlecock


class Notice_Set_Num:
    def __init__(self):
        self.image = load_image('resource/notice_set_num.png')
        self.font = load_font('resource/ENCR10B.TTF', 40)
        self.timer_set = False
    def draw(self):
        if server_competition.player1_set_score == 3:
            self.image.draw(400, 300)
            self.font.draw(255, 320, f'player1 win!!!', (255, 255, 255))
            self.font.draw(290, 260, f'press ESC', (255, 255, 255))
        if server_competition.player2_set_score == 3:
            self.image.draw(400, 300)
            self.font.draw(255, 320, f'player2 win!!!', (255, 255, 255))
            self.font.draw(290, 260, f'press ESC', (255, 255, 255))
    def update(self):
        if server_competition.player1_score == 5:
            server_competition.player1_set_score += 1
            self.reset()

        if server_competition.player2_score == 5:
            server_competition.player2_set_score += 1
            self.reset()

    def reset(self):
        server_competition.player1_score, server_competition.player2_score = 0, 0
        game_world.remove_object(self)

        #  셔틀콕과 플레이어 위치 초기화
        if server_competition.who_get_score == 'player1':
            self.x, self.y = 260, 265
        elif server_competition.who_get_score == 'player2':
            self.x, self.y = 540, 265
        server_competition.player1_x = 200
        server_competition.player2_x = 600
        game_world.add_object(self, 2)
        game_world.add_collision_pair('player1:shuttlecock', None, self)
        game_world.add_collision_pair('player2:shuttlecock', None, self)
        game_world.add_collision_pair('net:shuttlecock', None, self)

    def get_bb(self):
        return self.x - 10, self.y, self.x + 10, self.y + 220
