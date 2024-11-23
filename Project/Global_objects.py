class Global_objects:
    def __init__(self):
        self.player = None
        self.PlayerUI = None
        self.TimeUI = None
        
    def set_player(self,player):
        self.player = player
        
    def set_HPUI(self,UI):
        self.PlayerUI = UI
        
    def set_TimeUI(self,Time):
        self.TimeUI = Time

G_objects = Global_objects()