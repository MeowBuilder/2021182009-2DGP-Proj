from pico2d import *
import game_framework

# Run Speed
PIXEL_PER_METER = (64.0 / 1.0)
RUN_SPEED_KMPH = 5.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

class summon:
    Appear_sprite = None
    Death_sprite = None
    Idle_sprite = None
    player = None
    def __init__(self,Player,x = 640,y = 360):
        if summon.Appear_sprite is None:
            summon.Appear_sprite = load_image('./Asset/Boss/summonAppear.png')
        if summon.Death_sprite is None:
            summon.Death_sprite = load_image('./Asset/Boss/summonDeath.png')
        if summon.Idle_sprite is None:
            summon.Idle_sprite = load_image('./Asset/Boss/summonIdle.png')
        if summon.player is None:
            summon.player = Player
            
        self.x, self.y = x,y
        self.sx, self.sy = 0,0
        self.dead = False
        self.is_invincibility = False
        self.invincibility_time = 0
        self.speed = 1
        self.HP = 5
        self.dir = 0
        self.frame = 0
        
        self.Appear = True
        self.Appear_time = get_time()
        pass
    
    def update(self):
        self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        #여기부터 수정
        if self.Appear:
            if get_time() - self.Appear_time > 1:
                self.Appear_time = get_time()
                self.frame = self.frame + 1
                if self.frame == 6:
                    self.Appear = False
            pass
        elif not self.dead:
            self.frame = (self.frame + 1) % 4
            self.move_to_player(self.player)
        elif self.dead:
            if get_time() - self.Appear_time > 1:
                self.Appear_time = get_time()
                self.frame = self.frame + 1
                if self.frame == 6:
                    pass
            pass
        
    def draw(self):
        self.sx,self.sy = self.x - self.player.cur_map.window_left, self.y - self.player.cur_map.window_bottom
        if self.Appear:
            if self.dir < 0:
                self.Appear_sprite.clip_composite_draw(self.frame*50,0,50,50,0,'h',self.sx ,self.sy ,128,128)
            else:
                self.Appear_sprite.clip_composite_draw(self.frame*50,0,50,50,0,'w',self.sx ,self.sy ,128,128)
        elif not self.dead:
            if self.dir < 0:
                self.Idle_sprite.clip_composite_draw(self.frame*50,0,50,50,0,'h',self.sx ,self.sy ,128,128)
            else:
                self.Idle_sprite.clip_composite_draw(self.frame*50,0,50,50,0,'w',self.sx ,self.sy ,128,128)
        elif self.dead:
            if self.dir < 0:
                self.Death_sprite.clip_composite_draw(self.frame*50,0,50,50,0,'h',self.sx ,self.sy ,128,128)
            else:
                self.Death_sprite.clip_composite_draw(self.frame*50,0,50,50,0,'w',self.sx ,self.sy ,128,128)
            pass
    
    def get_attacked(self):
        if not self.is_invincibility and not self.dead:
            self.HP -= 1
            if not self.is_invincibility:
                self.is_invincibility = True
                self.invincibility_time = get_time()
            print(f'Summon HP : {self.HP}')
            
            if self.HP == 0:
                self.dead = True
                self.Appear_time = get_time()
            pass
        
    def move_to_player(self,Player):
        self.dir = ((Player.x-self.x)/max(1,abs(Player.x-self.x)))
        self.x += ((Player.x-self.x)/max(1,abs(Player.x-self.x))) * self.speed * RUN_SPEED_PPS * game_framework.frame_time
        self.y += ((Player.y-self.y)/max(1,abs(Player.y-self.y))) * self.speed * RUN_SPEED_PPS * game_framework.frame_time
        pass