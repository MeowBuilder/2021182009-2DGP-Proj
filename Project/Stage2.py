from pico2d import *
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_n:
            if Clear:
                game_framework.change_mode(Stage1)
        else:
            player.handle_events(event)

def get_player_info(origin):
    global player_info
    player_info = origin
    player_info.Enemy.clear()
    player_info.x,player_info.y = 640,360
    pass

def init():
    global Clear
    Clear = False
    
    global player
    player = Player(None)
    player.x,player.y = 640,360
    player.HP = player_info.HP
    player.Enemy.clear()
    worldmap = Map.Map(player)
    player.cur_map = worldmap

    boss_2 = Boss_2(player)
    player.Enemy.append(boss_2)
    playerUI = Player_HP(player)
    
    player.cur_stage = Stage2

    game_world.add_object(worldmap,0)
    game_world.add_object(player,2)
    game_world.add_object(boss_2,1)
    game_world.add_object(playerUI,3)
    
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

