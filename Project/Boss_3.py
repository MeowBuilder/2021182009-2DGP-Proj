import math
import Server

from pico2d import *
import random
import State_Machine
import game_framework
import game_world
import Stage3

from Speed_info import *
from Boss_3_Attack import Spike

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
        
        self.MAXHP = 50
        self.HP = self.MAXHP
        self.x, self.y = 1920/2, 1080/2 + 196
        self.sx, self.sy = 0,0
        self.speed = 1
        
        self.cur_pattern = Idle
        self.next_pattern = Attack1
        self.patterns = [Attack1,Teleport_in]
        
        self.pattern_num = 0
        self.idle_time = 0
        self.dir = 0
        self.is_invincibility = False
        self.invincibility_timer = 0
        self.invincibility_duration = 0.5
        self.is_skill_invincibility = False

        self.dead = False
        
        self.phase = 1
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        self.attack3_cooldown = 0.1
        
        self.SFX = load_wav('./Asset/SFX/StageClear.wav')
        self.SFX.set_volume(32)
        
    def load_image(self):
        if Boss_3.idle_sprite == None:
            Boss_3.idle_sprite = [load_image('./Asset/Boss_3/idle/idle%d.png'%i) for i in range(1,16)]
            Boss_3.attack1_sprite = [load_image('./Asset/Boss_3/attack1/attack%d.png'%i) for i in range(1,18)]
            Boss_3.attack2_sprite = [load_image('./Asset/Boss_3/attack2/attack%d.png'%i) for i in range(1,25)]
            Boss_3.attack3_sprite = [load_image('./Asset/Boss_3/attack3/attack%d.png'%i) for i in range(1,71)]
            Boss_3.attack4_sprite = [load_image('./Asset/Boss_3/attack4/attack%d.png'%i) for i in range(4,46)]
            Boss_3.attack5_sprite = [load_image('./Asset/Boss_3/attack5/attack%d.png'%i) for i in range(1,43)]
            Boss_3.teleport_in_sprite = [load_image('./Asset/Boss_3/teleport in/teleport in (%d).png'%i) for i in range(1,26)]
            Boss_3.teleport_out_sprite = [load_image('./Asset/Boss_3/teleport out/teleport out (%d).png'%i) for i in range(1,31)]
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
        
    def set_random_pattern(self):
        self.next_pattern = random.choice(self.patterns)
        pass

    def move_to_player(self,Player):
        self.dir = ((Player.x-self.x)/max(1,abs(Player.x-self.x)))
        self.x += ((Player.x-self.x)/max(1,abs(Player.x-self.x))) * self.speed * BossSpeed * game_framework.frame_time
        self.y += ((Player.y-self.y)/max(1,abs(Player.y-self.y))) * self.speed * BossSpeed * game_framework.frame_time
        pass
    
    def dead_func(self):
        Server.player.Enemy.remove(self)
        game_world.remove_object(self)
        Stage3.Clear = True
        pass
    
    def get_bb(self):
        return self.x - 56, self.y - 224, self.x + 56, self.y + 48
    
    def get_attacked(self):
        if self.state_machine.cur_state == Attack3:
            if Attack3.can_decrease:
                Attack3.own_frame -= 2
                Attack3.can_decrease = False
                self.attack3_cooldown = 0.1
            return
        if self.HP > 0:
            print(f'BOSS HP : {self.HP}')
            self.HP -= 1
            self.is_invincibility = True
            self.invincibility_timer = 0
            
            if self.HP == 0:
                self.state_machine.start(Die)
            elif self.HP <= self.MAXHP * 0.75 and self.phase == 1:
                self.state_machine.start(Attack4)
                self.phase = 2
            elif self.HP <= self.MAXHP * 0.5 and self.phase == 2:
                self.state_machine.start(Attack2)
                self.phase = 3
    
    def handle_collision(self,group,other):
        if group == 'player:attack':
            if not (self.is_invincibility or self.is_skill_invincibility):
                self.get_attacked()
        elif group == 'boss:attack':
            pass
        
    def teleport(self):
        self.x, self.y = random.randint(256,Server.Map.w - 256), random.randint(256,Server.Map.h - 256)
    
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
        
        if get_time() - Boss.idle_time > 5/Boss.phase:
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
        Boss.black_hole_created = False
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.black_hole_created = False
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        if int(Boss.frame) == len(Boss.attack1_sprite) // 2 and not Boss.black_hole_created:
            from Boss_3_Attack import Black_hole
            black_hole = Black_hole(Server.player.x, Server.player.y)
            game_world.add_object(black_hole, 1)
            
            if game_world.collision_pairs.get('player:black_hole'):
                game_world.collision_pairs['player:black_hole'][0].clear()
                game_world.collision_pairs['player:black_hole'][1].clear()
            
            game_world.add_collision_pair('player:black_hole', Server.player, black_hole)
            Boss.black_hole_created = True

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
        Boss.is_skill_invincibility = True
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.is_skill_invincibility = False
        Boss.patterns.append(Attack3)
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
        Attack3.own_frame = 0
        Attack3.can_decrease = True
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def do(Boss):
        Attack3.own_frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        Boss.frame = min(Attack3.own_frame, len(Boss.attack3_sprite) - 1)

        if Attack3.own_frame < 0:
            Boss.state_machine.start(Idle)
        elif int(Boss.frame) >= len(Boss.attack3_sprite) - 1:
            Server.player.HP = 0
            Server.player.player_died()
            Boss.state_machine.start(Idle)
            
        if not Attack3.can_decrease:
            Boss.attack3_cooldown -= game_framework.frame_time
            if Boss.attack3_cooldown <= 0:
                Attack3.can_decrease = True
    
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
        Boss.is_skill_invincibility = True
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.patterns.append(Attack5)
        Boss.is_skill_invincibility = False
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
        Boss.SFX.play()
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        
        if int(Boss.frame) >= len(Boss.death_sprite):
            Boss.dead_func()
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.death_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx ,Boss.sy ,512,512)
        else:
            Boss.death_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx ,Boss.sy ,512,512)

class Teleport_in:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        Boss.is_skill_invincibility = True
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.teleport()
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        
        if int(Boss.frame) >= len(Boss.teleport_in_sprite):
            Boss.state_machine.start(Teleport_out)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.teleport_in_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx ,Boss.sy ,512,512)
        else:
            Boss.teleport_in_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx ,Boss.sy ,512,512)

class Teleport_out:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.is_skill_invincibility = False
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        
        if int(Boss.frame) >= len(Boss.teleport_out_sprite):
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.teleport_out_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'h',Boss.sx ,Boss.sy ,512,512)
        else:
            Boss.teleport_out_sprite[int(Boss.frame)].clip_composite_draw(0,0,320,320,0,'w',Boss.sx ,Boss.sy ,512,512)