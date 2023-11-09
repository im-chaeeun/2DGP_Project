from pico2d import *

open_canvas()

character = load_image('character.png')

SCREEN_WIDTH = 800  # 스크린 사이즈 설정
SCREEN_HEIGHT = 600
x = SCREEN_WIDTH // 2
y = 150
running = True
dir = 0

def handle_events():
    global running, dir
    global x

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_RIGHT:
                dir += 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                dir += 1
            elif event.key == SDLK_RIGHT:
                dir -= 1


frame = 0

while running:
    clear_canvas()
    character.clip_draw(frame * 50, 100, 50, 50, x, y, 300, 300)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 5
    x += dir * 10
    delay(0.05)

close_canvas()