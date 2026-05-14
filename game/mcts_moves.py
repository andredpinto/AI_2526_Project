#for now its just a copy paste of what was in players
#i decided to keep everything the same and i will just expand our options in new files

import math
from game.board import Board
from game.data_storage import save_to_dataset
import random # nao vou fazer from random import choice, para ser mais claro quando eu usar esse metodo
#Class node for the monte carlo tree search that uses a list of moves instead of a list of states
class MoveNode:
    def __init__(self, state:Board, player, parent=None, child_limit=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.player = player #player que vai jogar a seguir
        self.unexpanded_children_states = None
        self.child_limit = child_limit

    def has_unexpanded_children_states(self):
        if self.state.isFinished(self.player):
            self.unexpanded_children_states = []

        elif self.unexpanded_children_states==None: # ainda so foi escolhido, nao explorado
            states= self.state.possible_states(self.player)
            random.shuffle(states)

            if self.child_limit: #não é None
                states = states[:self.child_limit] #in python there's no problem with child_limit being bigger than the length of the list

            self.unexpanded_children_states = states

        return len(self.unexpanded_children_states) > 0

    def uct(self, c=math.sqrt(2)):
        w = self.wins
        n = self.visits
        N = self.parent.visits
        return w/n + c*math.sqrt(math.log(N) / n) 

    #assume que unexpanded_children_states != None e de []
    def expand(self):
        children_state = self.unexpanded_children_states.pop()
        children_node = Node(children_state, self.player*-1, parent=self,child_limit=self.child_limit)
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

class MoveMCTS:
    def __init__(self, save_to_dataset=False, heuristic_win=False, heuristic_block_win=False,child_limit=None, save_tree=False,max_iter=300):
        """save_to_dataset - whether we save the move for the dataset or not\n
           heuristic_win - whether during simulation the mcts chooses the wining state\n
           heuristic_block_win - whether during simulation the mcts doesnt chose a wining state for the oponent\n
           save_tree - wheter the mcts keeps the tree or not\n
           max_iter - iters for the mcts
        """
        self.save_to_dataset = save_to_dataset
        self.heuristic_win = heuristic_win
        self.heuristic_block_win = heuristic_block_win
        self.child_limit = child_limit
        self.save_tree = save_tree
        self.max_iter=max_iter
        self.root = None

    #assumes board1 is one move ahead from board0
    @staticmethod #doesnt need the self argument, i will not put it outside the class, because its only used for the mcts
    def infer_move_by_diff(board0, board1):
        for col in range(board0.cols):
            h0 = board0.heights[col]
            h1 = board1.heights[col]
            if h1 == h0 + 1:
                return ("drop", col)
            if h1 == h0 - 1:
                return ("pop", col)

    def sync_tree(self, board, player):
        #se for a primeira jogada do jogo, criamos a raiz do zero ou se save_tree=False
        if self.root is None or not self.save_tree:
            self.root = Node(board, player, child_limit=self.child_limit)
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
        self.root = Node(board, player, child_limit=self.child_limit)

    def simulate(self, board, player):
        start_player = -player # o player é o jogador que vai jogar agora, ams nos queremos avaliar para o que levou ao estado atual
        #estado inicial -> tabulerio vazio->queremos esoclher a melhor jogada para o X, mas é o O a jogar

        while not board.isFinished(player):
            next_states = board.possible_states(player)
            winning_state = None
            bad_states = [] #para bloquear uam vitoria do adversario, eu pensei em so remover da lista next_states, mas convem nao modificar uma lista enquanto itero por ela

            for state in next_states:
                # verifica se este estado resulta numa vitória para o jogador atual
                if self.heuristic_win:
                    if state.winner(player) == player:
                        winning_state = state
                        break 

                #verifica se o estado resulta na vitoria do adversario(aquele caso especial de o pop fazer o adversario ganhar)
                #e se existe algum estado depois deste estado em que o opp pode ganhar
                if self.heuristic_block_win:
                    if state.winner(player)==-player:
                        bad_states.append(state) #caso especial do pop
                        continue
                    for opp_state in state.possible_states(-player):
                        if opp_state.winner(-player) ==-player:
                            bad_states.append(state)
                            break#este estado ja nao interessa, por tanto nao vamos explorar o resto dos estados que resultam deste

            if winning_state is not None:#é garantido só correr se heuristic_win=True, porque só assim é que entra dentro do if que pode mudar o None
                board = winning_state #escolhe a jogada vencedora

            elif self.heuristic_block_win:
                if len(bad_states)==len(next_states):
                    #igual ao else (todos os estados levam a uma possivel vitoria do adversario, duvido sobre a possibilidade disto acontecer but you never know)
                    board = random.choice(next_states) #como não ganha, escolhe uma jogada aleatória
                else:
                    good_states = [state for state in next_states if state not in bad_states]
                    board = random.choice(good_states if len(good_states) > 0 else next_states)

            else:
                board = random.choice(next_states) #como não ganha, escolhe uma jogada aleatória

            player *=-1

        winner = board.winner(player)
        if winner == 0:
            return 0
        if winner==start_player:
            return 1
        return -1 #bad for the player

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
            while not node.has_unexpanded_children_states(): #but this way i can still select a temrinal node(no children and no children to expand also)
                if (len(node.children)==0): #special case for terminal nodes
                    break
                node = node.best_uct_child()
            #expansao:
            if node.has_unexpanded_children_states(): # só se nao for terminal
                node = node.expand() #vai se expandir um dos filhos entao
            #simulacao:
            res = self.simulate(node.state, node.player)
            #e backprop:
            self.backpropagate(node, res)

        #escolha da melhor jogada
        best_child = self.root.best_n_child()

        #descobrimos qual foi o movimento feito para chegar a esse estado
        move = MCTS.infer_move_by_diff(self.root.state, best_child.state)

        #a raiz para a proxima jogada passa a ser este no
        if self.save_tree:
            self.root = best_child
            self.root.parent = None

        # guarda o estado e a decisao para treinar a arvore de decisao mais tarde
        if self.save_to_dataset:
            save_to_dataset(board, player, move)
        return move