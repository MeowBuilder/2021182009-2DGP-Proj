from pico2d import *

class Map:
    def __init__(self):
        self.size = (1280,720)
        self.map = load_image("./Asset/Map/Map_test.png")
    
    def update(self):
        pass
    
    def draw(self):
        self.map.draw(1280/2,720/2,1280,720)
        pass
    
    