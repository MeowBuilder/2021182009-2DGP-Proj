from pico2d import *
import State_Machine

class Player:
    def __init__(self):
        self.movement_sprite = [load_image('./Asset/Character/Front Movement.png'),load_image('./Asset/Character/Back Movement.png'),load_image('./Asset/Character/Side Movement.png')]
        self.attack_sprite = [load_image('./Asset/Character/Front ConsecutiveSlash.png'),load_image('./Asset/Character/Back ConsecutiveSlash.png'),load_image('./Asset/Character/Side ConsecutiveSlash.png')]
        self.dash_sprite = [load_image('./Asset/Character/Front DashnRoll.png'),load_image('./Asset/Character/Back Dash.png'),load_image('./Asset/Character/Side Dash.png')]
        self.frame = 0
        
        self.x,self.y = 400,300
        
        self.dir = [True,False,False,False] # 0:앞   1:뒤  2:오른쪽    3:왼쪽
        self.speed = 5
        
        self.state_machine = State_Machine.StateMachine(self)
        self.state_machine.start(Idle)
        
        self.attack_side = 0
        self.HP = 5
    def update(self):
        self.state_machine.update()
            
    def draw(self):
        self.state_machine.draw()

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


        
class Idle:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.movement_sprite[0].clip_draw(player.frame*64,64,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.movement_sprite[1].clip_draw(player.frame*64,64,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.movement_sprite[2].clip_draw(player.frame*64,64,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.movement_sprite[2].clip_composite_draw(player.frame*64,64,64,64,0,'h',player.x,player.y,128,128)
            pass
        player.frame = (player.frame + 1) % 6
    
    
class Move:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        if player.dir[0]:
            player.y -= player.speed
            pass
        if player.dir[1]:
            player.y += player.speed
            pass
        if player.dir[2]:
            player.x += player.speed
            pass
        if player.dir[3]:
            player.x -= player.speed
            pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.movement_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.movement_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.movement_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.movement_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
        player.frame = (player.frame + 1) % 6
        
class Attack_1:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.attack_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.attack_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.attack_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.attack_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
        
        player.frame = player.frame + 1
        
        if player.frame == 14:
            if player.attack_side == 0:
                player.frame = 0
                player.state_machine.start(Idle)
                player.state = 'idle'
            elif player.attack_side == 1:
                player.state_machine.start(Attack_2)
                player.state = 'attack_2'
                

class Attack_2:
    @staticmethod
    def enter(player):
        pass
    
    @staticmethod
    def exit(player):
        pass
    
    @staticmethod
    def do(player):
        pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.attack_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[1]:
            player.attack_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.attack_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.attack_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
        
        player.frame = player.frame + 1
        
        if player.frame == 21:
            if player.attack_side == 1:
                player.state_machine.start(Idle)
                player.state = 'idle'
                player.frame = 0
            elif player.attack_side == 2:
                player.attack_side = 0
                player.state_machine.start(Attack_1)
                player.state = 'attack'
                player.frame = 5
                
                
                
class Dash:
    @staticmethod
    def enter(player):
        player.frame = 0
        player.speed += 10
        pass
    
    @staticmethod
    def exit(player):
        player.speed -= 10
        player.frame = 0
        pass
    
    @staticmethod
    def do(player):
        if player.dir[0]:
            player.y -= player.speed
            pass
        if player.dir[1]:
            player.y += player.speed
            pass
        if player.dir[2]:
            player.x += player.speed
            pass
        if player.dir[3]:
            player.x -= player.speed
            pass
    
    @staticmethod
    def draw(player):
        if player.dir[0]:
            player.dash_sprite[0].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
        elif player.dir[1]:
            player.dash_sprite[1].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[2]:
            player.dash_sprite[2].clip_draw(player.frame*64,0,64,64,player.x,player.y,128,128)
            pass
        elif player.dir[3]:
            player.dash_sprite[2].clip_composite_draw(player.frame*64,0,64,64,0,'h',player.x,player.y,128,128)
            pass
        player.frame = player.frame + 1
        
        if player.frame == 3:
            player.state_machine.start(Move)
            player.state = 'move'      
                
                
                   