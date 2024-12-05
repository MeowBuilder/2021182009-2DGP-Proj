from pico2d import open_canvas, close_canvas
import game_framework

import Title as start_mode
import Boss_3

open_canvas(1280, 720)

init = Boss_3.Boss_3()
init.load_image()
del init

game_framework.run(start_mode)
close_canvas()

