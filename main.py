from pico2d import *

import game_framework
from mode import title_mode

# import play_mode_competition as start_mode
#import logo_mode as start_mode

from competition import play_mode_competition

open_canvas()
game_framework.run(title_mode)

close_canvas()