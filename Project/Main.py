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
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_m: # HP 닳기 확인용
                player.HP -= 1
            elif event.key == SDLK_s:
                player.switch_dir(0)
                player.switch_state(Move)
            elif event.key == SDLK_w:
                player.switch_dir(1)
                player.switch_state(Move)
            elif event.key == SDLK_d:
                player.switch_dir(2)
                player.switch_state(Move)
            elif event.key == SDLK_a:
                player.switch_dir(3)
                player.switch_state(Move)
            elif event.key == SDLK_LSHIFT:
                player.switch_state(Dash)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_s:
                if player.dir[0] and player.state_machine.cur_state == Move:
                    player.switch_state(Idle)
            elif event.key == SDLK_w:
                if player.dir[1] and player.state_machine.cur_state == Move:
                    player.switch_state(Idle)
            elif event.key == SDLK_d:
                if player.dir[2] and player.state_machine.cur_state == Move:
                    player.switch_state(Idle)
            elif event.key == SDLK_a:
                if player.dir[3] and player.state_machine.cur_state == Move:
                    player.switch_state(Idle)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if player.state_machine.cur_state == Attack_1:
                    player.attack_side = 1
                elif player.state_machine.cur_state == Attack_2:
                    player.attack_side = 2
                else:
                    player.frame = 0
                    player.attack_side = 0
                    player.switch_state(Attack_1)
    

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