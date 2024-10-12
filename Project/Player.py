from pico2d import *

class Player:
    def __init__(self):
        self.movement_sprite = [load_image('./Asset/Character/Front Movement.png'),load_image('./Asset/Character/Back Movement.png'),load_image('./Asset/Character/Side Movement.png')]
        self.attack_sprite = [load_image('./Asset/Character/Front ConsecutiveSlash.png'),load_image('./Asset/Character/Back ConsecutiveSlash.png'),load_image('./Asset/Character/Side ConsecutiveSlash.png')]
        self.frame = 0
        self.x,self.y = 400,300
        self.dir = [True,False,False,False] # 0:앞   1:뒤  2:오른쪽    3:왼쪽
        self.speed = 5
        self.state = 'attack' # idle / move / dash / attack
        
    def update(self):
        if self.state == 'move':
            if self.dir[0]:
                self.y -= self.speed
                pass
            if self.dir[1]:
                self.y += self.speed
                pass
            if self.dir[2]:
                self.x += self.speed
                pass
            if self.dir[3]:
                self.x -= self.speed
                pass
            
    def draw(self):
        if self.state == 'move':
            draw_move(self)
        elif self.state == 'idle':
            draw_idle(self)
        elif self.state == 'attack':
            draw_attack(self)
            
    def switch_dir(self,dir_index):
        self.frame = 0
        self.dir = [False,False,False,False]
        self.dir[dir_index] = True
        
        
def draw_move(self):
    if self.dir[0]:
        self.movement_sprite[0].clip_draw(self.frame*64,0,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[1]:
        self.movement_sprite[1].clip_draw(self.frame*64,0,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[2]:
        self.movement_sprite[2].clip_draw(self.frame*64,0,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[3]:
        self.movement_sprite[2].clip_composite_draw(self.frame*64,0,64,64,0,'h',self.x,self.y,128,128)
        pass
    self.frame = (self.frame + 1) % 6
    
def draw_idle(self):
    if self.dir[0]:
        self.movement_sprite[0].clip_draw(self.frame*64,64,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[1]:
        self.movement_sprite[1].clip_draw(self.frame*64,64,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[2]:
        self.movement_sprite[2].clip_draw(self.frame*64,64,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[3]:
        self.movement_sprite[2].clip_composite_draw(self.frame*64,64,64,64,0,'h',self.x,self.y,128,128)
        pass
    self.frame = (self.frame + 1) % 6
    
def draw_attack(self):
    if self.dir[0]:
        self.attack_sprite[0].clip_draw(self.frame*64,0,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[1]:
        self.attack_sprite[1].clip_draw(self.frame*64,0,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[2]:
        self.attack_sprite[2].clip_draw(self.frame*64,0,64,64,self.x,self.y,128,128)
        pass
    elif self.dir[3]:
        self.attack_sprite[2].clip_composite_draw(self.frame*64,0,64,64,0,'h',self.x,self.y,128,128)
        pass
    self.frame = (self.frame + 1) % 22
    if self.frame == 0:
        self.frame += 4