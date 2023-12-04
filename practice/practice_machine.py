from pico2d import load_image, load_font


class Practice_Machine:
    def __init__(self):
        self.image = load_image('resource/practice_machine.png')

    def draw(self):
        self.image.draw(630, 170)

    def update(self):
        pass