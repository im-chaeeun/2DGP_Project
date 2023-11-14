from pico2d import *

open_canvas()

character = load_image('character.png')
frame = 0

for x in range(0, 80, 1):
    clear_canvas()
    character.clip_draw(frame * 50, 0, 50, 50, 200, 200)
    update_canvas()
    frame = (frame + 1) % 5
    delay(0.05)
close_canvas()