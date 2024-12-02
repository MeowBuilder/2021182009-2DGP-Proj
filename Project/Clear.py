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
    global Clear_title
    global Clear_time
    global Font
    global Font_2
    Clear_title = load_image('./Asset/Clear/Clear_title.png')
    Clear_time = Server.TimeUI.time
    Font = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF',96)
    Font_2 = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF',48)
    pass

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    Clear_title.draw_to_origin(0,0,get_canvas_width(),get_canvas_height())
    Font.draw(get_canvas_width()/2 - 600,get_canvas_height()/2 - 150,'Clear Time : %.2f' %(Clear_time),(128,128,128))
    Font_2.draw(get_canvas_width()/2 - 450,get_canvas_height()/2 - 300,'Press Z to Return to Title',(256,256,256))
    update_canvas()

def pause():
    pass

def resume():
    pass

def move_to_next_stage():
    game_framework.change_mode(Title)
    pass