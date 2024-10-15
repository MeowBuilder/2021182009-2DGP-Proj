from pico2d import *
import State_Machine

class Boss:
    def __init__(self):
        self.idle_sprite = load_image('./Asset/Boss/idle.png')
        self.frame = 0
        
        self.HP = 10
        self.x, self.y = 640, 360
        self.cur_pattern = 0
        self.next_pattern = 1
        
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
        pass
    
    @staticmethod
    def exit(Boss):
        pass
    
    @staticmethod
    def do(Boss):
        Boss.frame = (Boss.frame + 1) % 4
    
    @staticmethod
    def draw(Boss):
        Boss.idle_sprite.clip_composite_draw(Boss.frame*100,0,100,100,0,'h',Boss.x,Boss.y,128,128)
