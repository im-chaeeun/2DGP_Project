from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time
import game_framework
from competition import play_mode_competition
from practice import play_mode_practice
from mode import title_mode


def init():
    global image
    global running
    global logo_start_time

    running = True
    image = load_image('resource/tuk_credit.png')
    logo_start_time = get_time()
    pass

def finish():
    pass

def update():
    global running
    if title_mode.mode == 1:
        if get_time() - logo_start_time >= 1.5:
            game_framework.change_mode(play_mode_practice)
    elif title_mode.mode == 2:
        if get_time() - logo_start_time >= 1.5:
            game_framework.change_mode(play_mode_competition)


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    pass
