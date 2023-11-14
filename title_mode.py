from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time, SDL_KEYDOWN,  SDLK_ESCAPE, SDLK_SPACE
import game_framework
import logo_mode
import play_mode


def init():
    global image
    image = load_image('title_screen.png')
    pass

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(800//2, 600//2, 800, 600)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(logo_mode)

    pass