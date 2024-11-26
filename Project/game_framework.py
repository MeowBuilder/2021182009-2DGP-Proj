import time

from pico2d import get_time

import Server
import Player
from UI import Player_HP, Time


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False

def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()
    
    global frame_time
    frame_time = 0.0
    current_time = time.time()
    
    global game_time
    game_time = get_time()

    Server.player = Player.Player(None)
    Server.PlayerUI = Player_HP(Server.player)
    Server.TimeUI = Time()

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time

    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
