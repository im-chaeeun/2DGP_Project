from pico2d import load_image


class Shuttlecock_Practice:
    image = None
    def __init__(self):
        self.image = load_image('resource/shuttlecock.png')




    def draw(self):
        # 코트 왼쪽에 있을 때 셔틀콕 그리기

        self.image.clip_composite_draw(0, 0, 7, 8, 0, ' ', 50, 50, 28, 32)
        self.image.clip_composite_draw(0, 0, 7, 8, 20, ' ', 100, 50, 28, 32)
        self.image.clip_composite_draw(0, 0, 7, 8, 50, ' ', 150, 50, 28, 32)
        self.image.clip_composite_draw(0, 0, 7, 8, 90, ' ', 200, 50, 28, 32)
        self.image.clip_composite_draw(0, 0, 7, 8, 130, ' ', 250, 50, 28, 32)
        self.image.clip_composite_draw(0, 0, 7, 8, -130, ' ', 300, 50, 28, 32)