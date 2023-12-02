from pico2d import *

import game_framework
import play_mode_competition
import play_mode_practice
import title_mode

#import play_mode_competition as start_mode
#import logo_mode as start_mode

open_canvas()
game_framework.run(play_mode_competition)

close_canvas()