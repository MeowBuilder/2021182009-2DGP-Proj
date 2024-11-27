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

def init():
    Clear_time = Server.TimeUI.time
    print(f'{Clear_time=}')
    pass

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

def move_to_next_stage():
    game_framework.change_mode(Title)
    pass