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

    # a funcao do humano vai verificar por ela propria se a jogada é valida, assim como o acontece com as ias
    # nao faz sentido estar a verificar aqui também
    def run(self):
        while (True):
            print(self.b)
            players[self.cur_player](self.b, self.cur_symbol)
            if self.b.isFinished():
                print("this is the end, cant say anything more for now :p")
                return
            self.cur_symbol*=-1
