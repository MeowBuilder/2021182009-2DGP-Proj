import math
from pico2d import *
import random
import State_Machine

class Boss:
    def __init__(self,Player):
        self.idle_sprite = load_image('./Asset/Boss/idle.png')
        self.attack_sprite = load_image('./Asset/Boss/attacking.png')
        self.skill_sprite = load_image('./Asset/Boss/skill1.png')
        self.frame = 0
        
        self.HP = 10
        self.x, self.y = 640, 720
        self.sx, self.sy = 0,0
        self.speed = 2
        self.cur_pattern = Idle
        self.next_pattern = Attack
        self.patterns = [Attack]
        self.idle_time = 0
        self.dir = 0
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        
        self.player = Player
        pass

    def update(self):
        self.state_machine.update()
        self.move_to_player(self.player)
        
    def draw(self):
        self.sx,self.sy = self.x - self.player.cur_map.window_left, self.y - self.player.cur_map.window_bottom
        self.state_machine.draw()
        
    def set_random_pattern(self):
        self.next_pattern = random.choice(self.patterns)
        pass
    
    def move_to_player(self,Player):
        self.dir = ((Player.x-self.x)/max(1,abs(Player.x-self.x)))
        self.x += ((Player.x-self.x)/max(1,abs(Player.x-self.x))) * self.speed
        self.y += ((Player.y-self.y)/max(1,abs(Player.y-self.y))) * self.speed
        pass
    
    
class Idle:
    @staticmethod
    def enter(Boss):
        Boss.idle_time = 0
        pass
    
    @staticmethod
    def exit(Boss):
        pass
    
    @staticmethod
    def do(Boss):
        Boss.idle_time += 0.5
        Boss.frame = (Boss.frame + 1) % 8
        
        if Boss.idle_time >= 30:
            Boss.state_machine.start(Boss.next_pattern)
            Boss.set_random_pattern()
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.idle_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'h',Boss.sx ,Boss.sy ,256,256)
        else:
            Boss.idle_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'w',Boss.sx ,Boss.sy ,256,256)
        
class Attack:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.player.is_invincibility = False
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + 1)
        if 5 < Boss.frame < 9:
            if math.sqrt((Boss.x - Boss.player.x) ** 2 + (Boss.y - Boss.player.y) ** 2) < 128:
                Boss.player.get_attacked()

        if Boss.frame == 13:
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'h',Boss.sx ,Boss.sy ,256,256)
        else:
            Boss.attack_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'w',Boss.sx ,Boss.sy ,256,256)
        
class Skill:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + 1)
        if Boss.frame == 12:
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.skill_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'h',Boss.sx ,Boss.sy ,256,256)
        else:
            Boss.skill_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'w',Boss.sx ,Boss.sy ,256,256)
