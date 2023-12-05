from pico2d import load_image, load_music

SCREEN_WIDTH = 800  # 스크린 사이즈 설정
SCREEN_HEIGHT = 600

class Court:
    def __init__(self):
        self.image = load_image('resource/badminton_court_background.png')
        # 배경 음악
        self.bgm = load_music('resource/cutiegirls.mp3')
        self.bgm.set_volume(50)
        self.bgm.repeat_play()
    def draw(self):
        self.image.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2)

    def update(self):
        pass
