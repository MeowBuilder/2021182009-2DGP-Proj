from asyncio import Server
from pico2d import *
import Server
import Title
import game_framework

import game_world

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            move_to_next_stage()

def init():
    Server.init()
    Server.TimeUI.pause_time = True
    global Gameover_title
    global Font
    global Font_2
    Gameover_title = load_image('./Asset/Title/Gameover_title.png')
    Font = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF',48)
    pass

def finish():
    game_world.clear()
    Server.player.Reset()
    Server.TimeUI.pause_time = False
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    Gameover_title.draw_to_origin(0,0,get_canvas_width(),get_canvas_height())
    Font.draw(get_canvas_width()/2 - 250,get_canvas_height()/2 - 100,'Press Z to Return',(256,128,128))
    update_canvas()

def pause():
    pass

def resume():
    pass

def move_to_next_stage():
    game_framework.change_mode(Server.player.cur_stage)
    pass