from pico2d import draw_rectangle


class Net:
    def __init__(self):
        self.x = 400
        self.y = 50

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y, self.x + 10, self.y + 220