from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time
import game_framework
import play_mode


def init():
    global image
    global running
    global logo_start_time

    running = True
    image = load_image('tuk_credit.png')
    logo_start_time = get_time()
    pass

def finish():
    pass

def update():
    global running
    if get_time() - logo_start_time >= 1.5:
        game_framework.change_mode(play_mode)
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    pass
