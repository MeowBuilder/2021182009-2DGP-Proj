from pico2d import *
from Player import *
from UI import *
import threading

# func
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_m: # HP 닳기 확인용
            player.HP -= 1
        else:
            player.handle_events(event)
    

def update_world():
    for o in world:
        o.update()
    render_world()
    
    if running:
        threading.Timer(0.05,update_world).start()
    pass

def render_world():
    clear_canvas()
    
    for o in world:
        o.draw()
    playerUI.draw(player)
    
    update_canvas()
    pass

# init
def reset_world():
    global world
    global running
    global player
    global playerUI
    
    running = True
    world = []
    
    player = Player()
    world.append(player)
    
    playerUI = Player_HP()
    pass

# main
def main():
    open_canvas(1920,1080,full=False)
    reset_world()
    
    update_world()
    
    while running:
        handle_events()
    
    close_canvas()
    pass

if __name__ == "__main__":
    main()