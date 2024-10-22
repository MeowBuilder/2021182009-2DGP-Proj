from pico2d import *

class Map:
    def __init__(self,Player):
        self.size = (1280,720)
        self.map = load_image("./Asset/Map/Map_test.png")
        self.x,self.y = 400,300
        self.player = Player
    def update(self):
        self.x = self.player.x
        self.y = self.player.y
        pass
    
    def draw(self):
        self.map.clip_draw(self.player.world_x,self.player.world_y,640,360,640,360,1280,720)
        pass
    
    