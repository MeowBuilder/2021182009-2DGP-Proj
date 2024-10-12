from pico2d import *
from Player import *
import threading

# func
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_s:
                player.switch_dir(0)
                player.state = 'move'
            elif event.key == SDLK_w:
                player.switch_dir(1)
                player.state = 'move'
            elif event.key == SDLK_d:
                player.switch_dir(2)
                player.state = 'move'
            elif event.key == SDLK_a:
                player.switch_dir(3)
                player.state = 'move'
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_s:
                if player.dir[0]:
                    player.state = 'idle'
            elif event.key == SDLK_w:
                if player.dir[1]:
                    player.state = 'idle'
            elif event.key == SDLK_d:
                if player.dir[2]:
                    player.state = 'idle'
            elif event.key == SDLK_a:
                if player.dir[3]:
                    player.state = 'idle'
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                player.state = 'attack'
    

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
    
    update_canvas()
    pass

# init
def reset_world():
    global running
    global player
    global world
    
    running = True
    world = []
    
    player = Player()
    world.append(player)
    pass

# main
def main():
    open_canvas()
    reset_world()
    
    update_world()
    
    while running:
        handle_events()
    
    close_canvas()
    pass

if __name__ == "__main__":
    main()