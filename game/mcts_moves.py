import math
from game.board import Board
from game.data_storage import save_to_dataset
import random 
from game.utils import *
"""
This mcts will have expansion policies, in other words the possible moves that a node can expand will be 
determined by the function we define
"""

#Class node for the monte carlo tree search that uses a list of moves instead of a list of states
class MoveNode:
    def __init__(self, state:Board, player, parent=None, child_limit=None, causal_move=None, expansion_policy=get_all_moves):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.player = player #player que vai jogar a seguir
        self.unexpanded_children_moves = None
        self.child_limit = child_limit
        self.causal_move = causal_move #the move that brought this node to life (to remove the infer_move_by_diff function i created)
        self.expansion_policy = expansion_policy

    def has_unexpanded_children_moves(self):
        if self.state.isFinished(self.player):
            self.unexpanded_children_moves = []

        elif self.unexpanded_children_moves==None: # ainda so foi escolhido, nao explorado
            moves = self.expansion_policy(self.state, self.player)
            random.shuffle(moves)

            if self.child_limit: #não é None
                moves = moves[:self.child_limit] #in python there's no problem with child_limit being bigger than the length of the list

            self.unexpanded_children_moves = moves

        return len(self.unexpanded_children_moves) > 0

    def uct(self, c=math.sqrt(2)):
        w = self.wins
        n = self.visits
        N = self.parent.visits
        return w/n + c*math.sqrt(math.log(N) / n) 

    #assume que unexpanded_children_moves != None e de []
    def expand(self):
        children_move = self.unexpanded_children_moves.pop()
        children_state = self.state.copy()
        children_state.apply_move(children_move[0], children_move[1], self.player)
        children_node = MoveNode(children_state, self.player*-1, parent=self,child_limit=self.child_limit,
        expansion_policy=self.expansion_policy, causal_move=children_move)
        self.children.append(children_node)
        return children_node

    #assumes it has children
    def best_uct_child(self):
        max = -2147483648
        best_node = None
        for child in self.children:
            tmp = child.uct()
            if tmp>max:
                max = tmp
                best_node = child
        return best_node
    
    #returns the child with the highest number of visits
    def best_n_child(self):
        max = -2147483648
        best_node = None
        for child in self.children:
            tmp = child.visits
            if tmp>max:
                max = tmp
                best_node = child
        return best_node

#the block_win (it's not really an heuristic) needs to use the list of possible states
class MoveMCTS:
    def __init__(self, save_to_dataset=False, heuristic_win=False, heuristic_block_win=False,child_limit=None, save_tree=False,max_iter=300,
    expansion_policy=get_all_moves, cycle_detection=False, max_depth=False, depth=60, use_minimax=False, minimax_agent=None, normalize_minimax=True):
        """save_to_dataset - whether we save the move for the dataset or not\n
           heuristic_win - whether during simulation the mcts chooses the wining state\n
           heuristic_block_win - whether during simulation the mcts doesnt chose a wining state for the oponent\n
           save_tree - wheter the mcts keeps the tree or not\n
           max_iter - iters for the mcts\n
           expansion_policy - function that defines what moves will be expanded (has to return a list with the moves has tuples) utils.py\n
           max_depth - whether we will be stopping the simulation when it surpasses a given "depth" value\n
           depth- what was said above\n
           use_minimax- whether we will use minimax evaluation instead of simulation\n
           minimax_agent= the actual minimax function\n
            normalize_minimax= whether the minimax value is used directly on backpropagation or if its normalized to -1, 1 or 0 only
        """
        self.save_to_dataset = save_to_dataset
        self.heuristic_win = heuristic_win
        self.heuristic_block_win = heuristic_block_win
        self.child_limit = child_limit
        self.save_tree = save_tree
        self.max_iter=max_iter
        self.root = None
        self.expansion_policy=expansion_policy
        self.cycle_detection = cycle_detection
        self.max_depth = max_depth
        self.depth = depth
        self.use_minimax=use_minimax
        self.minimax_agent=minimax_agent
        self.normalize_minimax=normalize_minimax
        if use_minimax:
            assert callable(self.minimax_agent.minimax)


    def sync_tree(self, board, player):
        #se for a primeira jogada do jogo, criamos a raiz do zero ou se save_tree=False
        if self.root is None or not self.save_tree:
            self.root = MoveNode(board, player, child_limit=self.child_limit, expansion_policy=self.expansion_policy)
            return

        # precisamos de encontrar qual dos filhos da arvore anterior 
        # corresponde ao estado atual do tabuleiro-depois da jogada do humano
        curr_hash = board.hash_state(player)

        for child in self.root.children:
            if child.state.hash_state(player) == curr_hash:
                self.root = child
                self.root.parent = None # cortamos a ligaçao
                return#fuck readibility for some lines of code deleted hahaha

        #se o humano fez uma jogada que nao tinhamos explorado
        self.root = MoveNode(board, player, child_limit=self.child_limit, expansion_policy=self.expansion_policy)

    def simulate(self, board, player):
        if self.use_minimax:
            score = self.minimax_agent.minimax(board, 0, -math.inf, math.inf, player)
            if self.normalize_minimax:
                if score > 0:
                    return 1
                if score < 0:
                    return -1
                return 0
            else: #returns the actual value the minimax returns
                return score
        start_player = -player # o player é o jogador que vai jogar agora, ams nos queremos avaliar para o que levou ao estado atual
        #estado inicial -> tabulerio vazio->queremos esoclher a melhor jogada para o X, mas é o O a jogar
        sim_board = board.copy()

        moves_count=0
        if self.cycle_detection:
            state_counts={}

        while not sim_board.isFinished(player):

            if self.max_depth and moves_count>=self.depth:
                return 0 #empate
            
            if self.cycle_detection:
                state_hash = sim_board.hash_state(player)
                state_counts[state_hash] = state_counts.get(state_hash,0) +1
                if state_counts[state_hash]==3:
                    return 0 # empate
            
            next_moves = sim_board.possible_moves(player)
            if not next_moves: return 0

            chosen_move = None

            if self.heuristic_win:
                for move in next_moves:
                    new_board = sim_board.copy()
                    new_board.apply_move(move[0], move[1], player) 

                    if new_board.winner(player)==player:
                        chosen_move = move
                        break
            
            if chosen_move is None and self.heuristic_block_win:
                good_moves = []

                for move in next_moves:
                    test_board = sim_board.copy()
                    test_board.apply_move(move[0], move[1], player)

                    if test_board.winner(player) == -player:
                        continue

                    opponent_can_win = False
                    for opp_move in test_board.possible_moves(-player):
                        opp_board = test_board.copy()
                        opp_board.apply_move(opp_move[0], opp_move[1], -player)
                        if opp_board.winner(-player) == -player:
                            opponent_can_win = True
                            break

                    if not opponent_can_win:
                        good_moves.append(move)

                if good_moves:
                    chosen_move = random.choice(good_moves)

            if chosen_move is None:
                chosen_move = random.choice(next_moves)

            sim_board.apply_move(chosen_move[0], chosen_move[1], player)
            player *= -1
            moves_count += 1
#=======end while===============================================
        winner = sim_board.winner(player)
        if winner == 0:
            return 0
        if winner==start_player:
            return 1
        return -1 #bad for the player
#end fsimulate============================================================

    def backpropagate(self, node, res):
        while node:
            node.visits +=1
            node.wins += res
            node = node.parent
            res = -res #o que é bom para um no passa a ser mau para o pai e vice versa
            # eu escolho sempre o maximo uct para selecionar

    def move(self, board, player):
        move = self.mcts(board, player)
        board.apply_move(move[0], move[1], player)

    def mcts(self, board, player):
        self.sync_tree(board, player) #trata de inicializar e/ou de salvar a tree, conforme o que se define no construtor

        for iter in range(self.max_iter):
            #comeca sempre na raiz
            node = self.root

            #selecao:
            # esoclher uma folha na arvore, para isso tenho de ir percorrendo a arvore ate chegar a um no com filhos nao expandidos
            while not node.has_unexpanded_children_moves(): #but this way i can still select a temrinal node(no children and no children to expand also)
                if (len(node.children)==0): #special case for terminal nodes
                    break
                node = node.best_uct_child()
            #expansao:
            if node.has_unexpanded_children_moves(): # só se nao for terminal
                node = node.expand() #vai se expandir um dos filhos entao
            #simulacao:
            res = self.simulate(node.state, node.player)
            #e backprop:
            self.backpropagate(node, res)

        #escolha da melhor jogada
        best_child = self.root.best_n_child()

        move = best_child.causal_move

        #a raiz para a proxima jogada passa a ser este no
        if self.save_tree:
            self.root = best_child
            self.root.parent = None

        # guarda o estado e a decisao para treinar a arvore de decisao mais tarde
        if self.save_to_dataset:
            save_to_dataset(board, player, move)
        return move
