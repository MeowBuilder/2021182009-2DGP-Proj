from pico2d import *

class UI:
    def __init__(self,UI_name):
        self.image = load_image('./Asset/UI/'+UI_name+'.png')
        self.x, self.y = 0,0
    def updatw(self):
        pass
    def draw(self):
        pass

        
class Player_HP(UI):
    def __init__(self):
        super().__init__('Player_HP')
    def draw(self,Player):
        self.image.clip_draw((5 - Player.HP) * 48,0,48,16,Player.sx,Player.sy + 48,96,32)
