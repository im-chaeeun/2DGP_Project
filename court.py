from pico2d import load_image


class Court:
    def __init__(self):
        self.image = load_image('badminton_court_background')

    def draw(self):
        self.image.draw(800, 600)

    def update(self):
        pass