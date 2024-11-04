class StateMachine:
    def __init__(self,o):
        self.o = o
        self.cur_state = None
        
    def start(self, state):
        if self.cur_state != None:
            self.cur_state.exit(self.o)
        self.cur_state = state
        self.cur_state.enter(self.o)
        
    def update(self):
        self.cur_state.do(self.o)
        
    def draw(self):
        self.cur_state.draw(self.o)

