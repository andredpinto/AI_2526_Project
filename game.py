#TODO falta saber quem ganha e se é empate
#TODO indicar tipos dos argumentos e o que as funcoes retornam
from board import Board
from players import players
class Game: #estado do jogo
    def __init__(self, player1, player2, rows=6, cols=7):
        self.b = Board(rows, cols)
        self.player1 = player1
        self.player2 = player2
        self.cur_player = player1 #which method to call
        self.cur_symbol= 1
        self.state_counts = {} # dict que salva o quantas vezes cada estado já apareceu

    # a funcao do humano vai verificar por ela propria se a jogada é valida, assim como o acontece com as ias
    # nao faz sentido estar a verificar aqui também
    def run(self):
        key = self.b.hash_state(self.cur_symbol)
        self.state_counts[key] = 1

        while (True):
            print(self.b)
            players[self.cur_player](self.b, self.cur_symbol)

            if self.b.isFinished(self.cur_symbol):
                print(self.b)
                winner = self.b.winner(self.cur_symbol)
                if (winner ==0): 
                    print("Empate!!!")
                elif (winner==1):
                    print("Player X won")
                else: # winner==-1
                    print("Player O won")
                return

            self.cur_symbol*=-1
            self.cur_player = self.player1 if self.cur_player==self.player2 else self.player2

            key = self.b.hash_state(self.cur_symbol)
            self.state_counts[key] = self.state_counts.get(key,0) +1 # se ainda nao havia a key retorna 0

            if self.b.is_full():
                print(self.b)
                if self.cur_player != "human": #the ai will always draw to prevent infinite games(consistent with what needs to happen in mcts vs mcts)
                    print("The AI choose to draw")
                    print("Draw!!!")
                    return
                #if human vs human: ask the current player
                choice = input("Board is full. Do you want to draw? (y/n)").strip().lower()
                if (choice=="y"):
                    print("Draw!!!")
                    return

            elif self.state_counts[key]==3:
                print(self.b)
                if self.player1 != "human" or self.player2 != "human":
                    print("The AI choose to draw")
                    print("Draw!!!")
                    return
                choice = input("Same board was repeated 3 times. Any player wants to draw? (y/n)").strip().lower()
                if (choice=="y"): #even if it is invalid - its equal to "n"
                    print("Draw!!!") #from now on, i promise to only write in english
                    return
