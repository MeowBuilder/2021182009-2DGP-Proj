from pico2d import *
import Title
import game_framework
import game_world
from Clear_Time import Clear_Time

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE) or (event.type == SDL_KEYDOWN and event.key == SDLK_z):
            move_to_next_stage()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_c:
            clear_time_manager.clear_records()
            init()  # 기록 초기화 후 화면 갱신

def init():
    global Font_title, Font_records
    global records
    global clear_time_manager
    
    # 폰트 로드
    Font_title = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF', 64)
    Font_records = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF', 36)
    
    # Clear_Time 객체를 통해 기록 로드
    clear_time_manager = Clear_Time()
    records = clear_time_manager.get_all_times()
    
    # 시간 기준으로 정렬 (오름차순)
    records.sort(key=lambda x: x['time'])
    # 상위 10개만 유지
    records = records[:10]

def finish():
    game_world.clear()

def update():
    game_world.update()

def draw():
    clear_canvas()
    
    # 제목 출력
    Font_title.draw(get_canvas_width()//2 - 200, get_canvas_height() - 100, 'TOP 10 RECORDS', (255, 255, 255))
    
    # 기록 출력
    start_y = get_canvas_height() - 200
    for i, record in enumerate(records):
        minutes = int(record['time'] // 60)
        seconds = record['time'] % 60
        text = f"{i+1}. {minutes:02d}:{seconds:05.2f}"
        Font_records.draw(get_canvas_width()//2 - 150, start_y - i*50, text, (255, 255, 255))
    
    # 안내 메시지
    Font_records.draw(get_canvas_width()//2 - 450, 100, 'Press Z to Return to Title', (255, 255, 255))
    Font_records.draw(get_canvas_width()//2 - 450, 50, 'Press C to Clear Records', (255, 255, 255))
    
    update_canvas()

def pause():
    pass

def resume():
    pass

def move_to_next_stage():
    game_framework.change_mode(Title)