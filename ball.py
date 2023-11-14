from pico2d import load_image

class Ball:
    image = None

    def __int__(self, x = 220, y = 350, velocity = 2):
        if Ball.image == None:
            Ball.image = load_image('ball.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity