from pico2d import *
from Player import *

# class


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
            elif event.key == SDLK_DOWN:
                player.dir[0] = True
                player.state = 'move'
            elif event.key == SDLK_UP:
                player.dir[1] = True
                player.state = 'move'
            elif event.key == SDLK_RIGHT:
                player.dir[2] = True
                player.state = 'move'
            elif event.key == SDLK_LEFT:
                player.dir[3] = True
                player.state = 'move'
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_DOWN:
                player.dir[0] = False
                player.state = 'idle'
            elif event.key == SDLK_UP:
                player.dir[1] = False
                player.state = 'idle'
            elif event.key == SDLK_RIGHT:
                player.dir[2] = False
                player.state = 'idle'
            elif event.key == SDLK_LEFT:
                player.dir[3] = False
                player.state = 'idle'
    

def update_world():
    for o in world:
        o.update()
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
    
    while running:
        handle_events()
        update_world()
        render_world()
        delay(0.05)
    
    close_canvas()
    pass

if __name__ == "__main__":
    main()