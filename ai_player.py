class AIPlayer:
    icon = ""
    record = []
    possible_paths = []
    possible_results = []

    def __init__(self, i):
        self.icon = i

    def choose_pos(self, current_path):
        pass
    
    def make_move(self, current_path):
        pass
    
    def update_record(self, path):
        self.record.append(path)
    