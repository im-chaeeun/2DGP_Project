from pico2d import *

SCREEN_WIDTH = 800  # 스크린 사이즈 설정
SCREEN_HEIGHT = 600
class Court:
    def __init__(self):
        self.image = load_image('badminton_court_background.png')

    def draw(self):
        self.image.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2)

    def update(self):
        pass

class Player1:
    def __init__(self):
        self.x, self.y = 200, 200
        self.frame = 0
        self.image = load_image('character.png')

    def update(self):
        self.frame =  (self.frame + 1) % 5

    def draw(self):
        self.image.clip_draw(self.frame * 50, 100, 50, 50, self.x, self.y, 250, 250)

class Player2:
    def __init__(self):
        self.x, self.y = 600, 200
        self.frame = 0
        self.image = load_image('character.png')

    def update(self):
        self.frame =  (self.frame + 1) % 5

    def draw(self):
        self.image.clip_composite_draw(self.frame * 50, 100, 50, 50, 0, 'h', self.x, self.y, 250, 250)


def reset_world():
    global running
    global court
    global world

    running = True

    world=[]

    court = Court()
    world.append(court)

    player1 = Player1()
    world.append(player1)

    player2 = Player2()
    world.append(player2)
def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()

    for o in world:
        o.draw()

    update_canvas()

open_canvas()

# initialization code
reset_world()

# game main loop code
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

# finalization code

close_canvas()