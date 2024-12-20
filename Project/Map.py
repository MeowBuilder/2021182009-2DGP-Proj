from pico2d import *

import Server

class Map:
    def __init__(self,map_name):
        self.map = load_image("./Asset/Map/"+map_name+".png")
        self.cw,self.ch = get_canvas_width(),get_canvas_height()
        self.w, self.h = self.map.w,self.map.h
        
        self.window_left = clamp(0,int(Server.player.x)-self.cw // 2,self.w - self.cw - 1)
        self.window_bottom = clamp(0,int(Server.player.y)-self.ch // 2,self.h - self.ch - 1)
    def update(self):
        self.window_left = clamp(0,int(Server.player.x)-self.cw // 2,self.w - self.cw - 1)
        self.window_bottom = clamp(0,int(Server.player.y)-self.ch // 2,self.h - self.ch - 1)
        pass
    
    def draw(self):
        self.map.clip_draw_to_origin(self.window_left,self.window_bottom,self.cw,self.ch,0,0)
        pass
    
    