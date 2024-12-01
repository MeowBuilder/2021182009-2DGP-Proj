from pico2d import *
import Server
import game_world



class Spike:
    Spike_sprite = None
    Caution_sprite = None
    player = None
    def __init__(self,x = 640,y = 360):
        if Spike.Spike_sprite is None:
            Spike.Spike_sprite = load_image('./Asset/Boss_3/Spike/Spike.png')
        if Spike.Caution_sprite is None:
            Spike.Caution_sprite = load_image('./Asset/Boss_3/Spike/Caution.png')
            
        self.x, self.y = x,y
        self.sx, self.sy = 0,0
        self.frame = 0
        
        self.Appear = True
        self.Appear_time = get_time()
        self.blink_time = 0.0
        self.active = False
        self.height_ratio = 0.0
        self.disappearing = False
        
    def update(self):
        current_time = get_time() - self.Appear_time
        
        if self.Appear:
            if current_time < 1.0:
                self.blink_time = max(0.5 - current_time * 0.4, 0.1)
                self.frame = int((current_time / self.blink_time) % 2)
            else:
                self.Appear = False
                self.active = True
                game_world.add_collision_pair('player:spike', Server.player, self)
        elif self.active:
            if not self.disappearing:
                if current_time <= 1.1:
                    self.height_ratio = min((current_time - 1.0) * 10, 1.0)
                elif current_time > 1.3:
                    self.disappearing = True
                    self.Appear_time = get_time()
            else:
                disappear_time = get_time() - self.Appear_time
                self.height_ratio = max(1.0 - disappear_time * 10, 0.0)
                if self.height_ratio == 0.0:
                    game_world.remove_object(self)
                
    def draw(self):
        if self.Appear:
            if self.frame == 0:
                self.Caution_sprite.clip_draw(0,0,64,64,self.x - Server.Map.window_left, 
                                       self.y - Server.Map.window_bottom,128,128)
        elif self.active:
            visible_height = int(128 * self.height_ratio)
            
            self.Spike_sprite.clip_draw(
                0, 128 - visible_height,
                128, visible_height,
                self.x - Server.Map.window_left,
                (self.y - 64 + visible_height/2) - Server.Map.window_bottom,
                128, visible_height
            )
        
        bb = (self.get_bb()[0]- Server.Map.window_left, 
              self.get_bb()[1]- Server.Map.window_bottom, 
              self.get_bb()[2]- Server.Map.window_left, 
              self.get_bb()[3]- Server.Map.window_bottom)
        draw_rectangle(*bb)
    
    def get_bb(self):
        return self.x - 64, self.y - 64, self.x + 64, self.y + 64
    
    def handle_collision(self,group,other):
        pass
           
class Black_hole:
    Black_hole_sprite = None
    player = None
    def __init__(self,x = 640,y = 180):
        if Black_hole.Black_hole_sprite is None:
            Black_hole.Black_hole_sprite = [load_image('./Asset/Boss_3/teleport out/teleport out (%d).png'%i) for i in range(1,10)]
            
        self.x, self.y = x,y
        self.sx, self.sy = 0,0
        self.frame = 0
        self.start_time = get_time()
        self.active = True
        self.scale = 0.0
        self.state = 'appear'  # appear, stay, disappear
        
    def update(self):
        current_time = get_time() - self.start_time
        
        if self.state == 'appear':
            self.scale = min(current_time * 2.0, 1.0)
            if current_time >= 0.5:  # 0.5초동안 커짐
                self.state = 'stay'
                self.start_time = get_time()
                
        elif self.state == 'stay':
            current_time = get_time() - self.start_time
            if current_time >= 5.0:  # 1초동안 유지
                self.state = 'disappear'
                self.start_time = get_time()
                
        elif self.state == 'disappear':
            current_time = get_time() - self.start_time
            self.scale = max(1.0 - current_time * 2.0, 0.0)
            if self.scale <= 0.0:  # 0.5초동안 작아짐
                game_world.remove_object(self)
                
                
        self.frame = (self.frame + 1) % 9  # 항상 애니메이션 재생
                
    def draw(self):
        if self.active:
            size = 128 * self.scale
            self.Black_hole_sprite[self.frame].draw(
                self.x - Server.Map.window_left,
                self.y - Server.Map.window_bottom,
                size, size
            )
            
        bb = (self.get_bb()[0]- Server.Map.window_left, 
              self.get_bb()[1]- Server.Map.window_bottom, 
              self.get_bb()[2]- Server.Map.window_left, 
              self.get_bb()[3]- Server.Map.window_bottom)
        draw_rectangle(*bb)
    
    def get_bb(self):
        return self.x - 196, self.y - 196, self.x + 196, self.y + 196
    
    def handle_collision(self,group,other):
            pass
