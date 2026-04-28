import math
from board import Board
import random # nao vou fazer from random import choice, para ser mais claro quando eu usar esse metodo
# metese aqui um dicionario ao que corresponde cada nome que se escolhe para jogar no main
# e dps as funcoes correspondentes

# guardamos a raiz da árvore aqui
mcts_root = None

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

def simulate(board, player):
    start_player = -player # o player é o jogador que vai jogar agora, ams nos queremos avaliar para o que levou ao estado atual
    #estado inicial -> tabulerio vazio->queremos esoclher a melhor jogada para o X, mas é o O a jogar
    while not board.isFinished(player):
        next_states = board.possible_states(player)
        winning_state = None
        for state in next_states:
            # verifica se este estado resulta numa vitória para o jogador atual
            if state.winner(player) == player:
                winning_state = state
                break 
                
        if winning_state is not None:
            board = winning_state #escolhe a jogada vencedora
        else:
            board = random.choice(next_states) #como não ganha, escolhe uma jogada aleatória
        player *=-1
    winner = board.winner(player)
    if winner == 0:
        return 0
    if winner==start_player:
        return 1
    return -1 #bad for the player


def backpropagate(node, res):
    while node:
        node.visits +=1
        node.wins += res
        node = node.parent
        res = -res #o que é bom para um no passa a ser mau para o pai e vice versa
        # eu escolho sempre o maximo uct para selecionar

#assumes board1 is one move ahead from board0
def infer_move_by_diff(board0, board1):
    for col in range(board0.cols):
        h0 = board0.heights[col]
        h1 = board1.heights[col]
        if h1 == h0 + 1:
            return ("drop", col)
        if h1 == h0 - 1:
            return ("pop", col)

def mcts_move(board, player, max_iter=1000):
    move = mcts(board, player, max_iter)
    board.apply_move(move[0], move[1], player)

def sync_tree(board, player):
    global mcts_root
    
    #se for a primeira jogada do jogo, criamos a raiz do zero
    if mcts_root is None:
        mcts_root = Node(board, player)
        return

    # precisamos de encontrar qual dos filhos da arvore anterior 
    # corresponde ao estado atual do tabuleiro-depois da jogada do humano
    curr_hash = board.hash_state(player)
    
    found = False
    for child in mcts_root.children:
        if child.state.hash_state(player) == curr_hash:
            mcts_root = child
            mcts_root.parent = None # cortamos a ligaçao
            found = True
            break
            
    #se o humano fez uma jogada que nao tinhamos explorado
    if not found:
        mcts_root = Node(board, player)


def mcts(board, player, max_iter=1000):
    global mcts_root
    
    sync_tree(board, player)

    for iter in range(max_iter):
        #comeca sempre na raiz
        node = mcts_root

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
        res = simulate(node.state, node.player)
        #e backprop:
        backpropagate(node, res)

    #escolha da melhor jogada
    best_child = mcts_root.best_n_child()

    #descobrimos qual foi o movimento feito para chegar a esse estado
    move = infer_move_by_diff(mcts_root.state, best_child.state)
    
    #a raiz para a proxima jogada passa a ser este no
    mcts_root = best_child
    mcts_root.parent = None
    
    return move



# the functions need to be declared beforehand
players = {
    "human" : human_move,
    "mcts" : mcts_move,
}
