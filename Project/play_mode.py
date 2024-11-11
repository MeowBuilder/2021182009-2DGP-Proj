from pico2d import *
import game_framework

import game_world
from Player import *
from UI import *
from Boss import *
from summon import *
import Map
import threading

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_events(event)

def init():
    global running
    global player
    global playerUI
    global boss_1
    global worldmap
    global summon1

    player = Player(None)
    worldmap = Map.Map(player)
    player.cur_map = worldmap

    boss_1 = Boss(player)
    summon1 = summon(player)
    player.Enemy.append(boss_1)
    player.Enemy.append(summon1)
    playerUI = Player_HP(player)

    game_world.add_object(worldmap,0)
    game_world.add_object(player,2)
    game_world.add_object(boss_1,1)
    game_world.add_object(summon1,1)
    game_world.add_object(playerUI,3)

    pass


def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    draw()

    if game_framework.running:
        threading.Timer(0.05, update).start()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
