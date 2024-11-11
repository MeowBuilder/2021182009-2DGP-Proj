import math

from pico2d import *
import random
import State_Machine
import game_framework

# Run Speed
PIXEL_PER_METER = (64.0 / 1.0)
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

class Boss:
    def __init__(self,Player):
        self.idle_sprite = load_image('./Asset/Boss/idle.png')
        self.attack1_sprite = load_image('./Asset/Boss/attacking.png')
        self.attack2_sprite = load_image('./Asset/Boss/skill1.png')
        self.under50_sprite = load_image('./Asset/Boss/summon.png')
        self.death_sprite = load_image('./Asset/Boss/death.png')
        self.frame = 0
        
        self.HP = 10
        self.x, self.y = 640, 720
        self.sx, self.sy = 0,0
        self.speed = 1
        self.cur_pattern = Idle
        self.next_pattern = Attack1
        self.patterns = [Attack1,Attack2]
        self.idle_time = 0
        self.dir = 0
        self.is_invincibility = False

        self.do_under50 = False
        self.dead = False
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        
        self.player = Player
        pass

    def update(self):
        if not self.dead:
            self.state_machine.update()
        
    def draw(self):
        if not self.dead:
            self.sx,self.sy = self.x - self.player.cur_map.window_left, self.y - self.player.cur_map.window_bottom
            self.state_machine.draw()
        
    def set_random_pattern(self):
        self.next_pattern = random.choice(self.patterns)
        pass
    
    def move_to_player(self,Player):
        self.dir = ((Player.x-self.x)/max(1,abs(Player.x-self.x)))
        self.x += ((Player.x-self.x)/max(1,abs(Player.x-self.x))) * self.speed * RUN_SPEED_PPS * game_framework.frame_time
        self.y += ((Player.y-self.y)/max(1,abs(Player.y-self.y))) * self.speed * RUN_SPEED_PPS * game_framework.frame_time
        pass

    def get_attacked(self):
        if not self.is_invincibility and not self.dead:
            self.HP -= 1
            self.is_invincibility = True
            print(f'BOSS HP : {self.HP}')
            
            if self.HP == 0:
                self.state_machine.start(Die)
            elif self.HP <= 5 and not self.do_under50:
                self.state_machine.start(under50_skill)
                self.do_under50 = True
            pass
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
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        Boss.move_to_player(Boss.player)
        if Boss.idle_time >= 30:
            Boss.state_machine.start(Boss.next_pattern)
            Boss.set_random_pattern()
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.idle_sprite.clip_composite_draw(int(Boss.frame)*100,0,100,100,0,'h',Boss.sx ,Boss.sy ,256,256)
        else:
            Boss.idle_sprite.clip_composite_draw(int(Boss.frame)*100,0,100,100,0,'w',Boss.sx ,Boss.sy ,256,256)
        
class Attack1:
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
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if 5 < Boss.frame < 9:
            if math.sqrt((Boss.x - Boss.player.x) ** 2 + (Boss.y - Boss.player.y) ** 2) < 128:
                Boss.player.get_attacked()

        if int(Boss.frame) == 13:
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack1_sprite.clip_composite_draw(int(Boss.frame) * 100, 0, 100, 100, 0, 'h', Boss.sx, Boss.sy, 256, 256)
        else:
            Boss.attack1_sprite.clip_composite_draw(int(Boss.frame) * 100, 0, 100, 100, 0, 'w', Boss.sx, Boss.sy, 256, 256)
        
class Attack2:
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
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if 4 < Boss.frame < 7:
            if math.sqrt((Boss.x - Boss.player.x) ** 2 + (Boss.y - Boss.player.y) ** 2) < 128:
                Boss.player.get_attacked()

        if int(Boss.frame) == 12:
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack2_sprite.clip_composite_draw(int(Boss.frame) * 100, 0, 100, 100, 0, 'h', Boss.sx, Boss.sy, 256, 256)
        else:
            Boss.attack2_sprite.clip_composite_draw(int(Boss.frame) * 100, 0, 100, 100, 0, 'w', Boss.sx, Boss.sy, 256, 256)


class under50_skill:
    @staticmethod
    def enter(Boss):
        print('enter under50')
        Boss.frame = 0
        Boss.is_invincibility = True
        Boss.start_time = get_time()
        pass

    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.is_invincibility = False
        pass

    @staticmethod
    def do(Boss):
        Boss.is_invincibility = True
        if get_time() - Boss.start_time >= 1 and Boss.frame >= 4:
            Boss.state_machine.start(Idle)
        elif get_time() - Boss.start_time >= 1:
            Boss.frame = (Boss.frame + 1)
            Boss.start_time = get_time()

    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.under50_sprite.clip_composite_draw(int(Boss.frame) * 100, 0, 100, 100, 0, 'h', Boss.sx, Boss.sy, 256, 256)
        else:
            Boss.under50_sprite.clip_composite_draw(int(Boss.frame) * 100, 0, 100, 100, 0, 'w', Boss.sx, Boss.sy, 256, 256)
            
class Die:
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
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(Boss.frame) == 19:
            Boss.dead = True
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.death_sprite.clip_composite_draw(int(Boss.frame)*100,0,100,100,0,'h',Boss.sx ,Boss.sy ,256,256)
        else:
            Boss.death_sprite.clip_composite_draw(int(Boss.frame)*100,0,100,100,0,'w',Boss.sx ,Boss.sy ,256,256)
