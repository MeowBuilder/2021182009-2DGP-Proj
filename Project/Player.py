from pico2d import *
import State_Machine
import game_framework

from Speed_info import *


class Player:
    Enemy = []
    def __init__(self,cur_map):
        self.movement_sprite = [load_image('./Asset/Character/Front Movement.png'),load_image('./Asset/Character/Back Movement.png'),load_image('./Asset/Character/Side Movement.png')]
        self.attack_sprite = [load_image('./Asset/Character/Front ConsecutiveSlash.png'),load_image('./Asset/Character/Back ConsecutiveSlash.png'),load_image('./Asset/Character/Side ConsecutiveSlash.png')]
        self.dash_sprite = [load_image('./Asset/Character/Front DashnRoll.png'),load_image('./Asset/Character/Back Dash.png'),load_image('./Asset/Character/Side Dash.png')]
        self.frame = 0
        
        self.x,self.y = 640,360
        self.sx,self.sy = get_canvas_width() // 2,get_canvas_height() // 2
        
        self.dir = [True,False,False,False] # 0:앞   1:뒤  2:오른쪽    3:왼쪽
        self.speed = 1
        self.cur_map = cur_map
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)

        self.cur_stage = None
        
        self.is_invincibility = False
        self.attack_side = 0
        self.HP = 5
    def update(self):
        self.state_machine.update()
        self.x = clamp(0,self.x,self.cur_map.cw)
        self.y = clamp(0,self.y,self.cur_map.ch)
            
    def draw(self):
        self.sx,self.sy = self.x - self.cur_map.window_left, self.y - self.cur_map.window_bottom
        self.state_machine.draw()
        
    def handle_events(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_DOWN:
                self.switch_dir(0)
                self.switch_state(Move)
            elif event.key == SDLK_UP:
                self.switch_dir(1)
                self.switch_state(Move)
            elif event.key == SDLK_RIGHT:
                self.switch_dir(2)
                self.switch_state(Move)
            elif event.key == SDLK_LEFT:
                self.switch_dir(3)
                self.switch_state(Move)
            elif event.key == SDLK_LSHIFT:
                self.switch_state(Dash)
            elif event.key == SDLK_z:
                if self.state_machine.cur_state == Attack_1:
                    self.attack_side = 1
                elif self.state_machine.cur_state == Attack_2:
                    self.attack_side = 2
                else:
                    self.switch_state(Attack_1)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_DOWN:
                if self.dir[0] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
            elif event.key == SDLK_UP:
                if self.dir[1] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
            elif event.key == SDLK_RIGHT:
                if self.dir[2] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
            elif event.key == SDLK_LEFT:
                if self.dir[3] and self.state_machine.cur_state == Move:
                    self.switch_state(Idle)
                

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

    def get_attacked(self):
        if not self.is_invincibility:
            self.HP -= 1
            self.is_invincibility = True
            
            if self.HP <= 0:
                self.player_died()
            pass

    def do_attack(self):
        for enemy in self.Enemy:
            if self.in_range(enemy):
                enemy.get_attacked()
            pass
        
    def player_died(self):
        self.cur_stage.finish()
        self.cur_stage.init()
        pass
        
    def in_range(self,Other, range = 128):
        return math.sqrt((Other.x - self.x) ** 2 + (Other.y - self.y) ** 2) < range

    def move(self):
        if self.dir[0]:
            self.y -= self.speed * PlayerSpeed * game_framework.frame_time
            pass
        if self.dir[1]:
            self.y += self.speed * PlayerSpeed * game_framework.frame_time
            pass
        if self.dir[2]:
            self.x += self.speed * PlayerSpeed * game_framework.frame_time
            pass
        if self.dir[3]:
            self.x -= self.speed * PlayerSpeed * game_framework.frame_time

class Idle:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.movement_sprite[0].clip_draw(int(player.frame)*64,64,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[1]:
            player.movement_sprite[1].clip_draw(int(player.frame)*64,64,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[2]:
            player.movement_sprite[2].clip_draw(int(player.frame)*64,64,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[3]:
            player.movement_sprite[2].clip_composite_draw(int(player.frame)*64,64,64,64,0,'h',player.sx,player.sy,128,128)
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
        player.move()
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.movement_sprite[0].clip_draw(int(player.frame)*64,0,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[1]:
            player.movement_sprite[1].clip_draw(int(player.frame)*64,0,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[2]:
            player.movement_sprite[2].clip_draw(int(player.frame)*64,0,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[3]:
            player.movement_sprite[2].clip_composite_draw(int(player.frame)*64,0,64,64,0,'h',player.sx,player.sy,128,128)
            pass
        
class Attack_1:
    @staticmethod
    def enter(player):
        player.frame = 0
        player.attack_side = 0
        pass
    
    @staticmethod
    def exit(player):
        for enemy in player.Enemy:
            enemy.is_invincibility = False
        pass
    
    @staticmethod
    def do(player):
        player.frame = player.frame + FRAMES_PER_ACTION * 2 * ACTION_PER_TIME * game_framework.frame_time
        if int(player.frame) == 14:
            if player.attack_side == 0:
                player.frame = 0
                player.state_machine.start(Idle)
                player.state = 'idle'
            elif player.attack_side == 1:
                player.state_machine.start(Attack_2)
                player.state = 'attack_2'

        if 5 < player.frame < 9:
            player.do_attack()
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.attack_sprite[0].clip_draw(int(player.frame) * 64, 0, 64, 64, player.sx, player.sy, 128, 128)
            pass
        elif player.dir[1]:
            player.attack_sprite[1].clip_draw(int(player.frame) * 64, 0, 64, 64, player.sx, player.sy, 128, 128)
            pass
        elif player.dir[2]:
            player.attack_sprite[2].clip_draw(int(player.frame) * 64, 0, 64, 64, player.sx, player.sy, 128, 128)
            pass
        elif player.dir[3]:
            player.attack_sprite[2].clip_composite_draw(int(player.frame) * 64, 0, 64, 64, 0, 'h', player.sx, player.sy, 128, 128)
            pass
        
class Attack_2:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        for enemy in player.Enemy:
            enemy.is_invincibility = False
        pass
    
    @staticmethod
    def do(player):
        player.frame = player.frame + FRAMES_PER_ACTION * 2 * ACTION_PER_TIME * game_framework.frame_time
        
        if int(player.frame) == 21:
            if player.attack_side == 1:
                player.state_machine.start(Idle)
                player.state = 'idle'
                player.frame = 0
            elif player.attack_side == 2:
                player.attack_side = 0
                player.state_machine.start(Attack_1)
                player.state = 'attack'
                player.frame = 5
                
        if 10 < player.frame < 18:
            player.do_attack()
            pass
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.attack_sprite[0].clip_draw(int(player.frame) * 64, 0, 64, 64, player.sx, player.sy, 128, 128)
            pass
        elif player.dir[1]:
            player.attack_sprite[1].clip_draw(int(player.frame) * 64, 0, 64, 64, player.sx, player.sy, 128, 128)
            pass
        elif player.dir[2]:
            player.attack_sprite[2].clip_draw(int(player.frame) * 64, 0, 64, 64, player.sx, player.sy, 128, 128)
            pass
        elif player.dir[3]:
            player.attack_sprite[2].clip_composite_draw(int(player.frame) * 64, 0, 64, 64, 0, 'h', player.sx, player.sy, 128, 128)
            pass
          
class Dash:
    @staticmethod
    def enter(player):
        player.is_invincibility = True
        player.frame = 0
        player.speed += 2
        
    @staticmethod
    def exit(player):
        player.is_invincibility = False
        player.speed -= 2
        player.frame = 0
        pass
    
    @staticmethod
    def do(player):
        player.move()
        
        player.frame = player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        
        if int(player.frame) == 3:
            player.state_machine.start(Move)
            player.state = 'move' 
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.dash_sprite[0].clip_draw(int(player.frame)*64,0,64,64,player.sx,player.sy,128,128)
        elif player.dir[1]:
            player.dash_sprite[1].clip_draw(int(player.frame)*64,0,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[2]:
            player.dash_sprite[2].clip_draw(int(player.frame)*64,0,64,64,player.sx,player.sy,128,128)
            pass
        elif player.dir[3]:
            player.dash_sprite[2].clip_composite_draw(int(player.frame)*64,0,64,64,0,'h',player.sx,player.sy,128,128)
            pass
        
