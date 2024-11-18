from pico2d import open_canvas, close_canvas
import game_framework

import Title as start_mode

open_canvas(800, 600)
game_framework.run(start_mode)
close_canvas()

