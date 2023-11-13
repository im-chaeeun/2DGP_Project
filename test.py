from pico2d import *

open_canvas()

character = load_image('character.png')

frame = 0

for x in range (0, 800, 5):
    clear_canvas()
    character.clip_draw(frame * 50, 50, 50, 50, 200, 200, 250, 250)
    update_canvas()
    frame = (frame + 1) % 2
    delay(0.5)

close_canvas()