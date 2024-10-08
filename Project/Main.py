from pico2d import *

# class
class Player:
    def __init__(self):
        self.image = load_image('./Asset/Character/Front Movement.png')
        self.frame = 0
        self.x,self.y = 400,300
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(self.frame*64,64,64,64,self.x,self.y,128,128)

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
            pass
        elif event.type == SDL_KEYUP:
            pass
    

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