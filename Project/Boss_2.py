import math

from pico2d import *
import random
import Stage2
import State_Machine
import game_framework
import game_world
import Server

from Speed_info import *

class Boss_2:
    def __init__(self):
        self.idle_sprite = load_image('./Asset/Boss_2/IDLE.png')
        self.move_sprite = load_image('./Asset/Boss_2/RUN.png')
        self.hurt_sprite = load_image('./Asset/Boss_2/HURT.png')
        self.attack_sprite = load_image('./Asset/Boss_2/ATTACK 1.png')
        self.frame = 0
        
        self.MAXHP = 40
        self.HP = self.MAXHP
        self.x, self.y = 1920/2, 1080/2
        self.sx, self.sy = 0,0
        self.speed = 1
        self.cur_pattern = Idle
        self.next_pattern = counter
        self.patterns = [counter,Attack1]
        self.idle_time = 0
        self.dir = 0
        self.is_invincibility = False
        self.invincibility_timer = 0
        self.invincibility_duration = 0.5  # 0.5초 무적
        self.is_skill_invincibility = False  # 스킬 사용 시 무적 상태를 따로 관리
        
        self.do_under50 = False
        self.dead = False
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        
        self.SFX = load_wav('./Asset/SFX/StageClear.wav')
        self.SFX.set_volume(32)
        pass

    def update(self):
        self.dir = ((Server.player.x-self.x)/max(1,abs(Server.player.x-self.x)))
        if self.is_invincibility:
            self.invincibility_timer += game_framework.frame_time
            if self.invincibility_timer >= self.invincibility_duration:
                self.is_invincibility = False
                self.invincibility_timer = 0
                
        if not len(Server.player.Enemy) == 1:
            self.is_invincibility = True
        
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

    def move_to_player(self):
        self.dir = ((Server.player.x-self.x)/max(1,abs(Server.player.x-self.x)))
        self.x += ((Server.player.x-self.x)/max(1,abs(Server.player.x-self.x))) * self.speed * BossSpeed * game_framework.frame_time
        self.y += ((Server.player.y-self.y)/max(1,abs(Server.player.y-self.y))) * self.speed * BossSpeed * game_framework.frame_time
        pass
    
    def get_attacked(self):
        if self.HP > 0:
            print(f'BOSS HP : {self.HP}')
            self.HP -= 1
            self.is_invincibility = True
            self.invincibility_timer = 0
            
            if self.HP == 0:
                self.state_machine.start(Die)
            elif self.HP <= self.MAXHP/2 and not self.do_under50:
                self.state_machine.start(under50_skill)
                self.do_under50 = True

    def dead_func(self):
        Server.player.Enemy.remove(self)
        game_world.remove_object(self)
        Stage2.Clear = True
        pass
    
    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32       
    
    def do_attack(self):
        if ((self.state_machine.cur_state == Attack1 and 5 < self.frame < 9) or 
            (self.state_machine.cur_state == counter_attack and 4 < self.frame < 7) or 
            (self.state_machine.cur_state == under50_skill and self.in_range) or
            (self.state_machine.cur_state == dash_attack and 3 < self.frame < 7)):
            game_world.collision_pairs['boss:attack'][0].clear()
            game_world.collision_pairs['boss:attack'][1].clear()
            game_world.add_collision_pair('boss:attack', self, Server.player)

    def end_attack(self):
        game_world.collision_pairs['boss:attack'][0].clear()
        game_world.collision_pairs['boss:attack'][1].clear()
    
    def handle_collision(self, group, other):
        if group == 'player:attack':
            if self.state_machine.cur_state == counter:
                self.state_machine.start(counter_attack)
            elif not (self.is_invincibility or self.is_skill_invincibility):
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
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        
        if get_time() - Boss.idle_time >= 2:
            if Server.player.in_range(Boss):
                Boss.state_machine.start(Boss.next_pattern)
                Boss.set_random_pattern()
            else:
                if dash_attack in Boss.patterns:
                    Boss.state_machine.start(dash_attack)
                else:
                    Boss.state_machine.start(Move)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.idle_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'h',Boss.sx ,Boss.sy +24,160,160)
        else:
            Boss.idle_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'w',Boss.sx ,Boss.sy +24,160,160)
         
class Move:
    @staticmethod
    def enter(Boss):
        Boss.move_time = get_time()
        pass
    
    @staticmethod
    def exit(Boss):
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        
        Boss.move_to_player()
        if get_time() - Boss.move_time >= 3.5:
            if Server.player.in_range(Boss):
                Boss.state_machine.start(Boss.next_pattern)
                Boss.set_random_pattern()
            else:
                Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.move_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'h',Boss.sx ,Boss.sy +24,160,160)
        else:
            Boss.move_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'w',Boss.sx ,Boss.sy +24,160,160)
        
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
        if 5 < Boss.frame < 7:
            Boss.do_attack()

        if int(Boss.frame) == 7:
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame) * 96, 0, 96, 96, 0, 'h', Boss.sx, Boss.sy +24, 160, 160)
        else:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame) * 96, 0, 96, 96, 0, 'w', Boss.sx, Boss.sy +24, 160, 160)
        
class counter:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        Boss.is_invincibility = True
        Boss.timer = get_time()
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.is_invincibility = False
        pass
    
    @staticmethod
    def do(Boss):
        if get_time() - Boss.timer >= 0.75:
            Boss.state_machine.start(Idle)
        pass
    
    @staticmethod
    def draw(Boss):
        time_passed = get_time() - Boss.timer
        if time_passed <= 0.25:
            if Boss.dir < 0:
                Boss.hurt_sprite.clip_composite_draw(0, 0, 96, 96, 0, 'h', Boss.sx, Boss.sy +24, 160, 160)
            else:
                Boss.hurt_sprite.clip_composite_draw(0, 0, 96, 96, 0, 'w', Boss.sx, Boss.sy +24, 160, 160)
        else:
            if Boss.dir < 0:
                Boss.attack_sprite.clip_composite_draw(0, 0, 96, 96, 0, 'h', Boss.sx, Boss.sy +24, 160, 160)
            else:
                Boss.attack_sprite.clip_composite_draw(0, 0, 96, 96, 0, 'w', Boss.sx, Boss.sy +24, 160, 160)

class counter_attack:
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
        Boss.is_invincibility = True
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if 3 < Boss.frame < 7:
            Boss.do_attack()

        if int(Boss.frame) == 7:
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame) * 96, 0, 96, 96, 0, 'h', Boss.sx, Boss.sy +24, 160, 160)
        else:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame) * 96, 0, 96, 96, 0, 'w', Boss.sx, Boss.sy +24, 160, 160)

class under50_skill:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        Boss.attack_count = 0
        Boss.in_range = False
        Boss.attack_time = get_time()
        Boss.is_invincibility = True
        Boss.is_skill_invincibility = True
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.is_invincibility = False
        Boss.is_skill_invincibility = False
        Boss.patterns.append(dash_attack)
        Boss.end_attack()
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if get_time() - Boss.attack_time <= 1.5:
            if Boss.frame >= 3.9:
                Boss.frame = 3
        elif get_time() - Boss.attack_time <= 2.0:
            if Boss.frame <= 6.0:
                if not Boss.in_range:
                    Boss.speed = 100
                    Boss.move_to_player()
                else:
                    Boss.speed = 1
                
                if Server.player.in_range(Boss, 32):
                    Boss.in_range = True
                    Boss.do_attack()
                
            if Boss.frame >= 6.9:
                Boss.frame = 6
                Boss.speed = 1
        else:
            Boss.attack_time = get_time()
            Boss.attack_count += 1
            Boss.frame = 0
            Boss.in_range = False
            Boss.end_attack()
            
            if Boss.attack_count >= 5:
                Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'h',Boss.sx ,Boss.sy +24,160,160)
        else:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'w',Boss.sx ,Boss.sy +24,160,160)

class dash_attack:
    @staticmethod
    def enter(Boss):
        Boss.frame = 0
        Boss.in_range = False
        Boss.attack_time = get_time()
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.end_attack()
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if get_time() - Boss.attack_time <= 1.5:
            if Boss.frame >= 3.9:
                Boss.frame = 3
        elif get_time() - Boss.attack_time <= 2.0:
            if Boss.frame <= 6.0:
                if not Boss.in_range:
                    Boss.speed = 100
                    Boss.move_to_player()
                else:
                    Boss.speed = 1
                
                if Server.player.in_range(Boss,16):
                    Boss.in_range = True
                    Boss.do_attack()
                
            if Boss.frame >= 6.9:
                Boss.frame = 6
                Boss.speed = 1
        else:
            Boss.state_machine.start(Idle)
            pass
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'h',Boss.sx ,Boss.sy +24,160,160)
        else:
            Boss.attack_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'w',Boss.sx ,Boss.sy +24,160,160)

class Die:
    @staticmethod
    def enter(Boss):
        Boss.frame = 3
        Boss.SFX.play()
        pass
    
    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame - FRAMES_PER_ACTION * (ACTION_PER_TIME * 1/10) * game_framework.frame_time)
        if Boss.frame <= 0:
            Boss.dead_func()
    
    @staticmethod
    def draw(Boss):
        if Boss.dir < 0:
            Boss.hurt_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'h',Boss.sx ,Boss.sy +24,160,160)
        else:
            Boss.hurt_sprite.clip_composite_draw(int(Boss.frame)*96,0,96,96,0,'w',Boss.sx ,Boss.sy +24,160,160)
