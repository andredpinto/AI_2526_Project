from board import Board
class Game: #estado do jogo 
    def __init__(self, player1, player2, rows=6, cols=7):
        self.b = Board(rows, cols)
        self.player1 = player1
        self.player2 = player2
        self.cur_player = player1

    def run(self):
        return
