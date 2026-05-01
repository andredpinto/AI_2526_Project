from board import Board
from players import players
from time import perf_counter #for the analysis

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

    def notebook_run(self) -> dict: #retorna estatisticas
        key = self.b.hash_state(self.cur_symbol)
        self.state_counts[key] = 1
        
        moves_player1 = 0
        moves_player2 = 0
        time_player1 = 0
        time_player2 = 0

        while (True):
            start = perf_counter()
            players[self.cur_player](self.b, self.cur_symbol)
            end = perf_counter()

            time = end-start
            if self.cur_symbol == 1:
                time_player1 += time
                moves_player1 += 1
            else:
                time_player2 += time
                moves_player2 += 1


            if self.b.isFinished(self.cur_symbol):
                winner = self.b.winner(self.cur_symbol)
                return {
                    "player1": self.player1,
                    "player2": self.player2,
                    "winner": winner,
                    "winner_name": self.player1 if winner == 1 else self.player2 if winner == -1 else "draw",

                    "time_player1": time_player1,
                    "time_player2": time_player2,
                    "avg_time_player1": time_player1 / moves_player1,
                    "avg_time_player2": time_player2 / moves_player2,
                }

            self.cur_symbol*=-1
            self.cur_player = self.player1 if self.cur_player==self.player2 else self.player2

            key = self.b.hash_state(self.cur_symbol)
            self.state_counts[key] = self.state_counts.get(key,0) +1 # se ainda nao havia a key retorna 0

            if self.b.is_full():
                return{
                    "player1": self.player1,
                    "player2": self.player2,
                    "winner": 0,
                    "winner_name": "draw",

                    "time_player1": time_player1,
                    "time_player2": time_player2,
                    "avg_time_player1": time_player1 / moves_player1,
                    "avg_time_player2": time_player2 / moves_player2,
                }

            elif self.state_counts[key]==3:
                return{
                    "player1": self.player1,
                    "player2": self.player2,
                    "winner": 0,
                    "winner_name": "draw",

                    "time_player1": time_player1,
                    "time_player2": time_player2,
                    "avg_time_player1": time_player1 / moves_player1,
                    "avg_time_player2": time_player2 / moves_player2,
                }
