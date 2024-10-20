from pico2d import *
import State_Machine

class Boss:
    def __init__(self):
        self.idle_sprite = load_image('./Asset/Boss/idle.png')
        self.attack_sprite = load_image('./Asset/Boss/attacking.png')
        self.frame = 0
        
        self.HP = 10
        self.x, self.y = 640, 360
        self.cur_pattern = 0
        self.next_pattern = 1
        self.idle_time = 0
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        pass

    def update(self):
        self.state_machine.update()
        
    def draw(self):
        self.state_machine.draw()
    
    
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
            Boss.state_machine.start(Attack)
    
    @staticmethod
    def draw(Boss):
        Boss.idle_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'h',Boss.x,Boss.y,256,256)
        
class Attack:
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
        if Boss.frame == 13:
            Boss.state_machine.start(Idle)
    
    @staticmethod
    def draw(Boss):
        Boss.attack_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'h',Boss.x,Boss.y,256,256)
