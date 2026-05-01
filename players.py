import math
from board import Board
from data_storage import save_to_dataset
import random # nao vou fazer from random import choice, para ser mais claro quando eu usar esse metodo
# metese aqui um dicionario ao que corresponde cada nome que se escolhe para jogar no main
# e dps as funcoes correspondentes

def human_move(board, player):
    while (True):
        move= input("drop/pop + collumn: ").lower().strip().split() #not case sensitive
        #o is_valid_move verifica por ele proprio se o user escreve drop ou pop
        #e vai verificar tbm se esta entre 0 e cols-1 (ou 1 e cols)
        if (len(move)!=2):
            print("Invalid move, try again")
            continue
        type = move[0]
        col = int(move[1])-1 # converter de 1->cols(o que o user escolhe) para 0->cols-1(indices do tabuleiro)
        if (board.is_valid_move(type, col, player)):
            board.apply_move(type, col, player)
            return
        else:
            print("Invalid move, try again")

#Class node for the monte carlo tree search
class Node:
    def __init__(self, state:Board, player, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.player = player #player que vai jogar a seguir
        self.unexpanded_children_states = None

    def has_unexpanded_children_states(self):
        if self.state.isFinished(self.player):
            self.unexpanded_children_states = []
        elif self.unexpanded_children_states==None: # ainda so foi escolhido, nao explorado
            self.unexpanded_children_states = self.state.possible_states(self.player)
        return len(self.unexpanded_children_states) > 0

    def uct(self, c=math.sqrt(2)):
        w = self.wins
        n = self.visits
        N = self.parent.visits
        return w/n + c*math.sqrt(math.log(N) / n) 

    #assume que unexpanded_children_states != None e de []
    def expand(self):
        children_state = self.unexpanded_children_states.pop()
        children_node = Node(children_state, self.player*-1, parent=self)
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

class MCTS:
    def __init__(self, save_to_dataset=False, heuristic_win=False, heuristic_block_win=False, save_tree=False, no_cycles=False,max_iter=2000):
        """save_to_dataset - whether we save the move for the dataset or not\n
           heuristic_win - whether during simulation the mcts chooses the wining state\n
           heuristic_block_win - whether during simulation the mcts doesnt chose a wining state for the oponent\n
           save_tree - wheter the mcts keeps the tree or not\n
           no_cycles - whether the mcts expands a children with a state already seen\n
           max_iter - iters for the mcts
        """
        self.save_to_dataset = save_to_dataset
        self.heuristic_win = heuristic_win
        self.heuristic_block_win = heuristic_block_win
        self.save_tree = save_tree
        self.no_cycles = no_cycles
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
            self.root = Node(board, player)
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
        self.root = Node(board, player)

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

            if winning_state is not None:
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
                    break;
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



# the functions need to be declared beforehand
players = {
    "human" : human_move,
    #how to test all of this? problema para depois
    "mcts_full" : MCTS(heuristic_win=True, heuristic_block_win=True, save_tree=True, no_cycles=True, max_iter=200).move,#block_win deixa muito lento
    "mcts_simplest":MCTS().move,
    "mcts_heuristic_win":MCTS(heuristic_win=True).move, #selects win state during simulation
    "mcts_heuristic_block_win" : MCTS(heuristic_block_win=True).move, #doesnt chose a move that lets the opponent win
    "mcts_no_cycles" : MCTS(no_cycles=True).move, #doesnt repeat states that are already in the tree
    "mcts_tree":MCTS(save_tree=True).move, #one of the above, but saving the tree
    #how many children we can select:
    #only test between them
    # "mcts_select_2_children" : mcts_move,
    # "mcts_select_4_children" : mcts_move,
    # "mcts_select_8_children" : mcts_move,
    # "mcts_select_all_children":mcts_move
}
