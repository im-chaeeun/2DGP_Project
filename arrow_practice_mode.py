from pico2d import load_image, load_font

import player_prcatice


class Arrow:
    def __init__(self):
        self.select_press = 0   # 0이면 아무것도 안 눌림
        self.image_left = load_image('arrow_left.png')
        self.image_left_press = load_image('arrow_left_press.png')

    def draw(self):
        # 선택 안 된 이미지는 다 그리고, 선택 되면 덮어 그리기!
         self.image_left.draw(50, 35)
        # if player_prcatice.Player.update(check_press_arrow) == 1:
        #     self.image_left_press.draw(50, 35)

    def update(self):
        pass