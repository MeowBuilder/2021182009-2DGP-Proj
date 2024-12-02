import time
import Player
from UI import Player_HP, Time


player = None
PlayerUI = None
TimeUI = None

Map = None

def is_None():
    return player is None and PlayerUI is None and TimeUI is None

def init():
    global player
    global PlayerUI
    global TimeUI
    if is_None():
        player = Player.Player()
        PlayerUI = Player_HP(player)
        TimeUI = Time()

def clear():
    global player
    global PlayerUI
    global TimeUI
    
    player = None
    PlayerUI = None
    TimeUI = None
    Map = None