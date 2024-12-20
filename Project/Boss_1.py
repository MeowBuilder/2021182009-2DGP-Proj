import math
import Server

from pico2d import *
import random
import State_Machine
import game_framework
import summon
import game_world
import Stage1

from Speed_info import *

class Boss_1:
    def __init__(self):
        self.idle_sprite = load_image('./Asset/Boss/idle.png')
        self.attack1_sprite = load_image('./Asset/Boss/attacking.png')
        self.attack2_sprite = load_image('./Asset/Boss/skill1.png')
        self.under50_sprite = load_image('./Asset/Boss/summon.png')
        self.death_sprite = load_image('./Asset/Boss/death.png')
        self.frame = 0
        
        self.MAXHP = 50
        self.HP = self.MAXHP
        self.x, self.y = 1920 // 2,1080 // 2
        self.sx, self.sy = 0,0
        self.speed = 1
        self.cur_pattern = Idle
        self.next_pattern = Attack1
        self.patterns = [Attack1,Attack2]
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
        self.SFX.set_volume(64)
        pass

    def update(self):
        self.dir = ((Server.player.x-self.x)/max(1,abs(Server.player.x-self.x)))
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
        Stage1.Clear = True
        pass
    
    def get_bb(self):
        return self.x - 64, self.y - 96, self.x + 72, self.y + 64
    
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
        pass
    
    def do_attack(self):
        if ((self.state_machine.cur_state == Attack1 and 5 < self.frame < 9) or 
            (self.state_machine.cur_state == Attack2 and 4 < self.frame < 7)):
            game_world.collision_pairs['boss:attack'][0].clear()
            game_world.collision_pairs['boss:attack'][1].clear()
            game_world.add_collision_pair('boss:attack', self, Server.player)

    def end_attack(self):
        game_world.collision_pairs['boss:attack'][0].clear()
        game_world.collision_pairs['boss:attack'][1].clear()
    
    def handle_collision(self, group, other):
        if group == 'player:attack':
            if not (self.is_invincibility or self.is_skill_invincibility) and len(Server.player.Enemy) == 1:
                self.get_attacked()
        elif group == 'boss:attack':
            pass

    def get_attack_bb(self):
        if self.state_machine.cur_state == Attack1 or self.state_machine.cur_state == Attack2:
            return self.x - 64, self.y - 64, self.x + 64, self.y + 64
        elif self.state_machine.cur_state == under50_skill:
            return self.x - 96, self.y - 96, self.x + 96, self.y + 96

class Idle:
    @staticmethod
    def enter(Boss):
        Boss.idle_time = get_time()
        Boss.is_invincibility = False
        Boss.is_skill_invincibility = False
        Boss.invincibility_timer = 0
        pass
    
    @staticmethod
    def exit(Boss):
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        Boss.move_to_player(Server.player)
        if get_time() - Boss.idle_time >= 5:
            Boss.state_machine.start(Boss.next_pattern)
            Boss.set_random_pattern()
            Boss.idle_time = get_time()
    
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
        Boss.end_attack()
        Boss.frame = 0
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if 5 < Boss.frame < 9:
            Boss.do_attack()

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
        Boss.end_attack()
        Boss.frame = 0
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if 4 < Boss.frame < 7:
            Boss.do_attack()

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
        Boss.is_skill_invincibility = True
        Boss.start_time = get_time()

    @staticmethod
    def exit(Boss):
        Boss.frame = 0
        Boss.is_invincibility = False
        Boss.is_skill_invincibility = False
        Boss.invincibility_timer = 0

    @staticmethod
    def do(Boss):
        if get_time() - Boss.start_time >= 1 and Boss.frame >= 4:
            Boss.is_invincibility = False
            Boss.is_skill_invincibility = False
            Boss.invincibility_timer = 0
            Boss.state_machine.start(Idle)
        elif get_time() - Boss.start_time >= 1:
            Boss.frame = (Boss.frame + 1)
            Boss.start_time = get_time()
            
            newenemy = summon.summon(Server.player,Boss.x + random.randint(-100,100),Boss.y + random.randint(-100,100))
            game_world.add_object(newenemy,1)
            Server.player.Enemy.append(newenemy)
            game_world.add_collision_pair('player:enemy',Server.player,newenemy)

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
        Boss.SFX.play()
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
            Boss.death_sprite.clip_composite_draw(int(Boss.frame)*100,0,100,100,0,'h',Boss.sx ,Boss.sy ,256,256)
        else:
            Boss.death_sprite.clip_composite_draw(int(Boss.frame)*100,0,100,100,0,'w',Boss.sx ,Boss.sy ,256,256)
