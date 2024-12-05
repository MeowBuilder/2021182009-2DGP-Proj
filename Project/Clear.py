from asyncio import Server
from pico2d import *
import Server
import Title
import game_framework
import game_world
from Clear_Time import Clear_Time

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
    global Clear_title, Clear_time, Font, Font_2
    global clear_time_manager
    
    Clear_title = load_image('./Asset/Title/Clear_title.png')
    Clear_time = Server.TimeUI.time
    Font = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF',96)
    Font_2 = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF',48)
    
    # 클리어 타임 저장 (초 단위로 저장)
    clear_time_manager = Clear_Time()
    clear_time_manager.add_time({'time': Clear_time})
    
    global music
    music = load_music('./Asset/Music/Clear_Music.mp3')
    music.set_volume(36)
    music.repeat_play()
    music.play()

def finish():
    music.stop()
    game_world.clear()
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    Clear_title.draw_to_origin(0,0,get_canvas_width(),get_canvas_height())
    
    # 분과 초로 변환하여 출력
    minutes = int(Clear_time // 60)
    seconds = Clear_time % 60
    Font.draw(get_canvas_width()/2 - 600, get_canvas_height()/2 - 150, 
             f'Clear Time : {minutes:02d}:{seconds:05.2f}', (128,128,128))
    
    Font_2.draw(get_canvas_width()/2 - 450,get_canvas_height()/2 - 300,
               'Press Z to Return to Title',(256,256,256))
    update_canvas()

def pause():
    pass

def resume():
    pass

def move_to_next_stage():
    game_framework.change_mode(Title)
    pass