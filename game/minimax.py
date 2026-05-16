import math
from game.utils import heuristic_win 
#class MiniMax for controlling parameters
class Minimax:
    def __init__(self, max_depth=3, heuristic=heuristic_win, pruning=True):
        self.max_depth = max_depth
        self.heuristic = heuristic
        self.pruning = pruning 
        """heuristic -> heuristics are defined in utils.py\n
        pruning -> alpha beta pruning"""
    
    #applies the move that reaches the child state with the best minimax eval
    def move(self, state, curr_player):
        moves = state.possible_moves(curr_player)
        best_move = None
        best_eval = -math.inf if curr_player==1 else math.inf

        for move in moves:
            new_state = state.copy()
            new_state.apply_move(move[0], move[1], curr_player)
            eval = self.minimax(new_state, 0, -math.inf, math.inf, -curr_player)

            if curr_player==1:
                if eval>best_eval:
                    best_eval=eval
                    best_move=move
            else:#curr_player==-1 / minimizing player
                if eval<best_eval:
                    best_eval=eval
                    best_move=move

        state.apply_move(best_move[0], best_move[1], curr_player)


    #https://www.youtube.com/watch?v=Aq5WXmQQooo fantastic video
    #reminder for later: we are using copies because the pop is not so easy to undo, undoing only drops would make the recursion stop working when a pop appears...i think
    def minimax(self, state, depth, alpha, beta, curr_player):
        """curr_player determines if its the maximizing turn or minimizing"""
        if depth==self.max_depth or state.isFinished(curr_player):
            return self.heuristic(state, curr_player)
        
        if curr_player==1:#max's turn
            max_eval=-math.inf
            for move in state.possible_moves(curr_player):
                new_state = state.copy()
                new_state.apply_move(move[0], move[1], curr_player)
                eval = self.minimax(new_state, depth+1, alpha, beta, -curr_player)
                max_eval = max(max_eval, eval)
                if self.pruning:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        
        else: #minimizing player, -1
            min_eval=math.inf
            for move in state.possible_moves(curr_player):
                new_state = state.copy()
                new_state.apply_move(move[0], move[1], curr_player)
                eval = self.minimax(new_state, depth+1, alpha, beta, -curr_player)
                min_eval = min(min_eval, eval)
                if self.pruning:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval