from pico2d import *

open_canvas()

character = load_image('chhracter.png')

frame = 0
for x in range(0, 800, 10):
    clear_canvas()
    character.clip_draw(frame * 50, 100, 50, 50, x, 150, 300, 300)
    update_canvas()
    frame = (frame + 1) % 5
    delay(0.05)
close_canvas()