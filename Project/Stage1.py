from asyncio import Server
from pico2d import *
import Server
import Stage1
import Stage2
import game_framework

import game_world
from Player import *
from UI import *
from Boss_1 import *
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
    resize_canvas(1280,720)
    Server.init()
        
    global Clear
    Clear = False

    Server.player.y = 0

    worldmap = Map.Map('Forest')
    Server.Map = worldmap
    
    boss = Boss_1()
    Server.player.Enemy.clear()
    Server.player.Enemy.append(boss)
    
    Server.player.cur_stage = Stage1

    game_world.add_collision_pair('player:boss',Server.player,boss)
    game_world.add_attack_collision_pairs()
    
    game_world.add_object(worldmap,0)
    game_world.add_object(Server.player,2)
    game_world.add_object(boss,1)
    game_world.add_object(Server.PlayerUI,3)
    game_world.add_object(Server.TimeUI,3)
    
    global music
    music = load_music('./Asset/Music/Stage1_Music.mp3')
    music.set_volume(36)
    music.repeat_play()
    music.play()
    pass

def finish():
    music.stop()
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()
    
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

def move_to_next_stage():
    game_framework.change_mode(Stage2)
    pass