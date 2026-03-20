from collections import deque


#tabuleiro de connect4 com var. de dar pop out
class Board:
    # lista de 7 deques para ser mais eficiente do que uma matriz ou lista
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        # lista de 6 deques=colunas
        self.b = [deque(maxlen=rows) for d in range(cols)]

    def drop(self, col, player):
        if len(self.b[col]) < self.rows:
            self.b[col].appendleft(player)  #adiciona sempre em cima (+ esquerda = + cima

    def pop(self, col):
        if (len(self.b[col]) > 0):
            self.b[col].pop() # tira do fundo (+direita = + fundo)

    def __str__(self): #o print pode nao ser tao eficiente o que importa são as ações para o mcts
        s = ""
        for i in range(self.rows): #para cada linha
            for j in range(self.cols): #para cada coluna
                if i < (self.rows - len(self.b[j])): # se ainda houver espacos livres na coluna
                    s += "-"
                else: # se nao comeca a colocar o tipo da coluna j na linha em que estamos menos as posicoes que estavam vazias
                    s += self.b[j][i -(self.rows - len(self.b[j]))]
            s += "\n"
        return s


if __name__ == "__main__":
    teste = Board()
    for i in range(4):
        teste.drop(1, "X")
    print(teste)
    for i in range(6):
        teste.pop(1)
    print(teste)
