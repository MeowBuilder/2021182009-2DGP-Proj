from pico2d import *
import State_Machine

class Player:
    def __init__(self):
        self.movement_sprite = [load_image('./Asset/Character/Front Movement.png'),load_image('./Asset/Character/Back Movement.png'),load_image('./Asset/Character/Side Movement.png')]
        self.attack_sprite = [load_image('./Asset/Character/Front ConsecutiveSlash.png'),load_image('./Asset/Character/Back ConsecutiveSlash.png'),load_image('./Asset/Character/Side ConsecutiveSlash.png')]
        self.dash_sprite = [load_image('./Asset/Character/Front DashnRoll.png'),load_image('./Asset/Character/Back Dash.png'),load_image('./Asset/Character/Side Dash.png')]
        self.frame = 0
        
        self.x,self.y = 400,300
        self.world_x, self.world_y = 640,360
        
        self.dir = [True,False,False,False] # 0:앞   1:뒤  2:오른쪽    3:왼쪽
        self.speed = 5
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        
        self.attack_side = 0
        self.HP = 5
    def update(self):
        self.state_machine.update()
            
    def draw(self):
        self.state_machine.draw()
        
    def handle_events(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_s:
                self.switch_dir(0)
                self.switch_state(Move)
            elif event.key == SDLK_w:
                self.switch_dir(1)
                self.switch_state(Move)
            elif event.key == SDLK_d:
                self.switch_dir(2)
                self.switch_state(Move)
            elif event.key == SDLK_a:
                self.switch_dir(3)
                self.switch_state(Move)
            elif event.key == SDLK_LSHIFT:
                self.switch_state(Dash)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_s:
                if self.dir[0] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
            elif event.key == SDLK_w:
                if self.dir[1] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
            elif event.key == SDLK_d:
                if self.dir[2] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
            elif event.key == SDLK_a:
                if self.dir[3] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if self.state_machine.cur_state == Attack_1:
                    self.attack_side = 1
                elif self.state_machine.cur_state == Attack_2:
                    self.attack_side = 2
                else:
                    self.frame = 0
                    self.attack_side = 0
                    self.switch_state(Attack_1)

    def switch_dir(self,dir_index):
        if self.state_machine.cur_state == Attack_2 or self.state_machine.cur_state == Dash:
            return
        
        self.frame = 0
        self.dir = [False,False,False,False]
        self.dir[dir_index] = True
        
    def switch_state(self, state):
        if self.state_machine.cur_state == Attack_2 or self.state_machine.cur_state == Dash:
            return
        
        self.state_machine.start(state)


class Idle:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 6
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.movement_sprite[0].clip_draw(player.frame*64,64,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.movement_sprite[1].clip_draw(player.frame*64,64,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.movement_sprite[2].clip_draw(player.frame*64,64,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.movement_sprite[2].clip_composite_draw(player.frame*64,64,64,64,0,'h',player.x,player.y,128,128)
            pass
    
class Move:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        if player.dir[0]:
            if(player.world_y - 180 - player.speed) >= 0:
                player.world_y -= player.speed
            else:
                player.y -= player.speed
            pass
        if player.dir[1]:
            if(player.world_y + 180 + player.speed) <= 720:
                player.world_y += player.speed
            else:
                player.y += player.speed
            pass
        if player.dir[2]:
            player.x += player.speed
            pass
        if player.dir[3]:
            player.x -= player.speed
            pass
        player.frame = (player.frame + 1) % 6
        
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.movement_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.movement_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.movement_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.movement_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
        
class Attack_1:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        player.frame = player.frame + 1
        if player.frame == 14:
            if player.attack_side == 0:
                player.frame = 0
                player.state_machine.start(Idle)
                player.state = 'idle'
            elif player.attack_side == 1:
                player.state_machine.start(Attack_2)
                player.state = 'attack_2'
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.attack_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.attack_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.attack_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.attack_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
        
class Attack_2:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        player.frame = player.frame + 1
        
        if player.frame == 21:
            if player.attack_side == 1:
                player.state_machine.start(Idle)
                player.state = 'idle'
                player.frame = 0
            elif player.attack_side == 2:
                player.attack_side = 0
                player.state_machine.start(Attack_1)
                player.state = 'attack'
                player.frame = 5
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.attack_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.attack_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.attack_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.attack_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
          
class Dash:
    @staticmethod
    def enter(player):
        player.frame = 0
        player.speed += 10
        
    @staticmethod
    def exit(player):
        player.speed -= 10
        player.frame = 0
        pass
    
    @staticmethod
    def do(player):
        if player.dir[0]:
            player.y -= player.speed
            pass
        if player.dir[1]:
            player.y += player.speed
            pass
        if player.dir[2]:
            player.x += player.speed
            pass
        if player.dir[3]:
            player.x -= player.speed
            pass
        
        player.frame = player.frame + 1
        
        if player.frame == 3:
            player.state_machine.start(Move)
            player.state = 'move' 
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.dash_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
        elif player.dir[1]:
            player.dash_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.dash_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.dash_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
        
