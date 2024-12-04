from pico2d import *
import time

import game_framework

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
        self.image.clip_draw((5 - self.player.HP) * 48,0,48,16,self.player.sx,self.player.sy + 48,96,32)
        
class Time:
    def __init__(self):
        self.Font = load_font('./Asset/Font/PF스타더스트 3.0 Bold.TTF',32)
        self.time = 0
        self.pause_time = False
        self.x,self.y = 640-100,680
        
    def update(self):
        if not self.pause_time:
            self.time += game_framework.frame_time
        
    def draw(self):
        self.Font.draw(self.x,self.y,'Time : %.2f' %(self.time/60),(255,255,255))
