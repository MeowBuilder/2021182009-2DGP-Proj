from pico2d import *
import Server
import Stage1
import Stage2
import game_framework

import game_world
from Player import *
from UI import *
from Boss_2 import *
from summon import *
import Map

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Server.player.handle_events(event)

def init():
    global Clear
    Clear = False
    
    Server.player.y = 0
    Server.player.Enemy.clear()
        
    worldmap = Map.Map(Server.player,'Dungeon')
    Server.player.cur_map = worldmap

    boss_2 = Boss_2()
    Server.player.Enemy.append(boss_2)
    
    Server.player.cur_stage = Stage2

    game_world.add_object(worldmap,0)
    game_world.add_object(Server.player,2)
    game_world.add_object(boss_2,1)
    game_world.add_object(Server.PlayerUI,3)
    game_world.add_object(Server.TimeUI,3)
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
    game_framework.change_mode(Stage1)