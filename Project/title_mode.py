from pico2d import *
import game_framework
import play_mode

LOOP_TIME = 3.0
FRAME_PER_LOOP = 15

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            game_framework.change_mode(play_mode)
        else:
            pass

def init():
    global title
    global frame
    frame = 0
    title = [load_image('./Asset/Title/Title-export' + '%d' %i + '.png') for i in range(1,16)]
    pico2d.resize_canvas(1580,725)
    pass

def finish():
    pass

def update():
    global frame
    frame = (frame + FRAME_PER_LOOP / LOOP_TIME * game_framework.frame_time) % 15
    pass

def draw():
    title[int(frame)].draw(1580/2,725/2)
    update_canvas()
    pass

def pause():
    pass

def resume():
    pass

