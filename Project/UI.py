from pico2d import *

class UI:
    def __init__(self,UI_name):
        self.image = load_image('./Asset/UI/'+UI_name+'.png')
        self.x, self.y = 0,0
    def update(self):
        pass
    def draw(self):
        pass

        
class Player_HP(UI):
    def __init__(self,Player):
        super().__init__('Player_HP')
        self.player = Player
    def draw(self):
        self.image.clip_draw((5 - self.player.HP) * 48,0,48,16,self.player.sx,self.player.sy + 80,96,32)