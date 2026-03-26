#TODO validar se a jogada é legal no proprio metodo(pop e drop) ou fora
class Board: #tabuleiro de connect4 com var. de dar pop out
    #possiveis otimizacoes:
        # usar numpy arrays?
        # colocar ints em vez de strings?
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.heights = [0] * cols
        self.b = [["-"] * rows for _ in range(cols)] # cada lista é uma coluna, por tanto primeiro acedemos as colunas e dps às linhas
        self.last_move = (-1, -1) #(col, row) quando se faz pop, o valor da linha fica -1

    def drop(self, col, player): # col toma valores de 0 a cols-1(6)
        h = self.heights[col]
        self.b[col][h] = player
        self.last_move = (col, h)
        self.heights[col] += 1

    def pop(self, col):
        for i in range(self.heights[col]-1):
            self.b[col][i] = self.b[col][i+1]
        self.b[col][self.heights[col]-1] = "-" #para nao aceder a zonas inexistentes no array
        self.heights[col] -=1
        self.last_move = (col,-1)

    # nao usar uma string para ser + eficiente?
    def __str__(self):
        s = ""
        for i in range(self.rows-1, -1, -1): #para imprimir temos de percorrer para cada linha
            for j in range(self.cols):       # todas as colunas
                s+= self.b[j][i]
            s += "\n"
        return s


if __name__ == "__main__":
    #so alguns testes:
    teste = Board()
    for i in range(4):
        teste.drop(1, "X")
    print(teste)
    for i in range(6):
        teste.pop(1)
    print(teste)
