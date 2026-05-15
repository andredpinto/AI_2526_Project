
#class MiniMax for controlling parameters
class Minimax:
    def __init__(max_depth=3, heuristic=heuristic_win, pruning=True):
        self.max_depth = max_depth
        self.heuristic = heuristic
        self.pruning = pruning 
        """heuristic -> heuristics are defined in utils.py\n
        pruning -> alpha beta pruning"""
    
    def minimax(state, depth, alpha, beta, player):
        ...