import math
import Server

from pico2d import *
import random
import State_Machine
import game_framework
import game_world
import Stage1

from Speed_info import *
from Spike import Spike

class Boss_3:
    idle_sprite = None
    attack1_sprite = None
    attack2_sprite = None
    attack3_sprite = None
    attack4_sprite = None
    attack5_sprite = None
    teleport_in_sprite = None
    teleport_out_sprite = None
    death_sprite = None
    
    def __init__(self):
        self.frame = 0
        
        self.MAXHP = 10
        self.HP = self.MAXHP
        self.x, self.y = 640, 720
        self.sx, self.sy = 0,0
        self.speed = 1
        self.cur_pattern = Idle
        self.next_pattern = Attack5
        self.patterns = [Attack1,Attack2,Attack3,Attack4,Attack5]
        self.pattern_num = 0
        self.idle_time = 0
        self.dir = 0
        self.is_invincibility = False
        self.invincibility_timer = 0
        self.invincibility_duration = 0.5
        self.is_skill_invincibility = False

        self.dead = False
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        pass
    
    def load_image(self):
        if Boss_3.idle_sprite == None:
            Boss_3.idle_sprite = [load_image('./Asset/Boss_3/idle/idle%d.png'%i) for i in range(1,16)]
            Boss_3.attack1_sprite = [load_image('./Asset/Boss_3/attack1/attack%d.png'%i) for i in range(1,18)]
            Boss_3.attack2_sprite = [load_image('./Asset/Boss_3/attack2/attack%d.png'%i) for i in range(1,25)]
            Boss_3.attack3_sprite = [load_image('./Asset/Boss_3/attack3/attack%d.png'%i) for i in range(1,71)]
            Boss_3.attack4_sprite = [load_image('./Asset/Boss_3/attack4/attack%d.png'%i) for i in range(4,46)]
            Boss_3.attack5_sprite = [load_image('./Asset/Boss_3/attack5/attack%d.png'%i) for i in range(1,43)]
            Boss_3.teleport_in_sprite = [load_image('./Asset/Boss_3/teleport in/teleport in%d.png'%i) for i in range(1,31)]
            Boss_3.teleport_out_sprite = [load_image('./Asset/Boss_3/teleport out/teleport out%d.png'%i) for i in range(1,26)]
            Boss_3.death_sprite = [load_image('./Asset/Boss_3/death/death%d.png'%i) for i in range(1,66)]
        pass

    def update(self):
        if self.is_invincibility:
            self.invincibility_timer += game_framework.frame_time
            if self.invincibility_timer >= self.invincibility_duration:
                self.is_invincibility = False
                self.invincibility_timer = 0

        if not self.dead:
            self.state_machine.update()

    def draw(self):
        if not self.is_invincibility or self.is_skill_invincibility or int(self.invincibility_timer * 10) % 2:
            if not self.dead:
                self.sx,self.sy = self.x - Server.Map.window_left, self.y - Server.Map.window_bottom
                self.state_machine.draw()
                bb = (self.get_bb()[0]- Server.Map.window_left, self.get_bb()[1]- Server.Map.window_bottom, self.get_bb()[2]- Server.Map.window_left, self.get_bb()[3]- Server.Map.window_bottom)
                draw_rectangle(*bb)
        
    def set_random_pattern(self):
        self.next_pattern = Attack5
        #self.next_pattern = random.choice(self.patterns)
        pass

    def move_to_player(self,Player):
        self.dir = ((Player.x-self.x)/max(1,abs(Player.x-self.x)))
        self.x += ((Player.x-self.x)/max(1,abs(Player.x-self.x))) * self.speed * BossSpeed * game_framework.frame_time
        self.y += ((Player.y-self.y)/max(1,abs(Player.y-self.y))) * self.speed * BossSpeed * game_framework.frame_time
        pass
    
    def dead_func(self):
        Server.player.Enemy.remove(self)
        game_world.remove_object(self)
        Stage1.Clear = True
        pass
    
    def get_bb(self):
        return self.x - 56, self.y - 224, self.x + 56, self.y + 48
    
    def get_attacked(self):
        print(f'BOSS HP : {self.HP}')
        self.HP -= 1
        self.is_invincibility = True
        self.invincibility_timer = 0
            
        if self.HP == 0:
            self.state_machine.start(Die)
    
    def do_attack(self):
        if Server.player.in_range(self,128):
            Server.player.get_attacked()
        pass
    
    def end_attack(self):
        game_world.collision_pairs['boss:attack'][0].clear()
        game_world.collision_pairs['boss:attack'][1].clear()
    
    def handle_collision(self,group,other):
        if group == 'player:attack':
            if not (self.is_invincibility or self.is_skill_invincibility):
                self.get_attacked()
        elif group == 'boss:attack':
            pass
    
class Idle:
    @staticmethod
    def enter(Boss):
        Boss.idle_time = get_time()
        pass
    
    @staticmethod
    def exit(Boss):
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 15
        
        if get_time() - Boss.idle_time > 5:
            Boss.state_machine.start(Boss.next_pattern)
            Boss.set_random_pattern()
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.idle_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx ,Boss.sy ,512,512)
        else:
            Boss.idle_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx ,Boss.sy ,512,512)
        
class Attack1:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.end_attack()
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        if int(Boss.frame) == len(Boss.attack1_sprite):
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack1_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx,Boss.sy,512,512)
        else:
            Boss.attack1_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx,Boss.sy,512,512)

class Attack2:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.end_attack()
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        if int(Boss.frame) == len(Boss.attack2_sprite):
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack2_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx,Boss.sy,512,512)
        else:
            Boss.attack2_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx,Boss.sy,512,512)
            
class Attack3:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.end_attack()
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        if int(Boss.frame) == len(Boss.attack3_sprite):
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack3_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx,Boss.sy,512,512)
        else:
            Boss.attack3_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx,Boss.sy,512,512)
            
class Attack4:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.end_attack()
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        if int(Boss.frame) == len(Boss.attack4_sprite):
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack4_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx,Boss.sy,512,512)
        else:
            Boss.attack4_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx,Boss.sy,512,512)
            
class Attack5:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        Boss.spike_timer = 0
        Boss.spike_delay = 0.5
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        
        Boss.spike_timer += game_framework.frame_time
        if Boss.spike_timer >= Boss.spike_delay:
            Boss.spike_timer = 0
            spike = Spike(Server.player.x, Server.player.y)
            game_world.add_object(spike, 1)

        if int(Boss.frame) == len(Boss.attack5_sprite):
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack5_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx,Boss.sy,512,512)
        else:
            Boss.attack5_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx,Boss.sy,512,512)

         
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
            Boss.dead_func()
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.death_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx ,Boss.sy ,512,512)
        else:
            Boss.death_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx ,Boss.sy ,512,512)
