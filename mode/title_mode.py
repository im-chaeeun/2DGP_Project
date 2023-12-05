from pico2d import load_image, clear_canvas, update_canvas, get_events, SDL_KEYDOWN, SDLK_ESCAPE, load_music, load_font
from sdl2 import SDLK_2, SDLK_1

import game_framework
from mode import logo_mode


def init():
    global image, bgm

    image = load_image('resource/title_screen.png')

    bgm = load_music('resource/football.mp3')
    bgm.set_volume(50)
    bgm.repeat_play()
    pass

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(800//2, 600//2, 800, 600)
    font = load_font('resource/ENCR10B.TTF', 35)
    font.draw(155, 200, 'PRESS1 - Practice Mode', (255, 255, 255))
    font.draw(155, 160, 'PRESS2 - Competition Mode', (255, 255, 255))

    update_canvas()
    pass

def handle_events():
    global mode
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            mode = 1
            game_framework.change_mode(logo_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            mode = 2
            game_framework.change_mode(logo_mode)

    pass