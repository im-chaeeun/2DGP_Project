from pico2d import load_image

SCREEN_WIDTH = 800  # 스크린 사이즈 설정
SCREEN_HEIGHT = 600

class Court:
    def __init__(self):
        self.image = load_image('badminton_court_background.png')

    def draw(self):
        self.image.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2)

    def update(self):
        pass
