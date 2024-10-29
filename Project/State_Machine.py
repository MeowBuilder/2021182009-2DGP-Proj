# 이벤트 체크함수
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_DOWN, SDLK_UP


def space_down(e): # e가 space down인지 판단
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e): # e가 타임아웃인지 판단
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def start_event(e):
    return e[0] == 'START'

class StateMachine:
    def __init__(self,obj):
        self.obj = obj
        self.cur_state = None
        self.event_q = []
        pass

    def start(self,state):
        self.cur_state = state
        self.cur_state.enter(self.obj, ('START',0))
        pass

    def update(self):
        self.cur_state.do(self.obj)
        if self.event_q:# list는 멤버가 있으면 True
            e = self.event_q.pop(0)
            self.handle_event(e)
            pass
        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e):
        self.event_q.append(e)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                self.cur_state.exit(self.obj,e)
                self.cur_state = next_state
                self.cur_state.enter(self.obj,e)
                return
        #print(f'        WARNING: {e}not handled at state {self.cur_state}')
        pass