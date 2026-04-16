#TODO validar se a jogada é legal no proprio metodo(pop e drop) ou fora
class Board: #tabuleiro de connect4 com var. de dar pop out
    #possiveis otimizacoes:
        # usar numpy arrays?
    def __init__(self, rows=6, cols=7, board=None):
        self.rows = rows
        self.cols = cols
        self.heights = [0] * cols
        if board==None:
            self.b = [[0 ] * rows for _ in range(cols)] # cada lista é uma coluna, por tanto primeiro acedemos as colunas e dps às linhas
        else: self.b = board
        self.last_move = (-1, -1) #(col, row) quando se faz pop, o valor da linha fica -1

    def drop(self, col, player:int): # col toma valores de 0 a cols-1(6)
        h = self.heights[col]
        self.b[col][h] = player
        self.last_move = (col, h)
        self.heights[col] += 1

    def pop(self, col):
        for i in range(self.heights[col]-1):
            self.b[col][i] = self.b[col][i+1]
        self.b[col][self.heights[col]-1] = 0 #para nao aceder a zonas inexistentes no array
        self.heights[col] -=1
        self.last_move = (col,-1)

    def __str__(self):
        dict = {0:"-", 1:"X", -1:"O"}
        s = "|1|2|3|4|5|6|7|\n---------------\n"
        for i in range(self.rows-1, -1, -1): #para imprimir temos de percorrer para cada linha
            s+="|"
            for j in range(self.cols):       # todas as colunas
                s+= dict[self.b[j][i]]
                s+="|"
            s += "\n"
        s+="---------------\n"
        return s
    
    def isFinished(self) -> bool:
        #TODO: Case where pop creates tow 4-in-a-rows: player who made the pop wins;
        # Case where board is full and player decides to end the game
        # Finnaly, draw case: same state repeated 3 times (either player can declare draw)
        # Estas são as regras descritas no documento
        # Talvez seja preciso adicionar uma variável para perceber de quem é o turno
        if self.last_move[0]==-1: return False  # No plays yet; change this if initialization is changed
        col = self.last_move[0]
        row = self.last_move[1]
        if row != -1:    # last move was an insertion, safe to check only the insertion spot
            return self._pos_checker(col, row)
        else:   # check all of the rows in the col
            for i in range(self.heights[col]):
                if self._pos_checker(col, i): return True
        return False

    def _pos_checker(self, col:int, row:int) -> bool:    # the _ supposed to represent that this is a private method
        # checks if position (col, line) contains 4 (or more) of the same elements in a row
        # assumes self.b[col][line] is a valid position
        player = self.b[col][row]
        if player == 0: return False
        directions = ((1,0), (0,1), (1,1), (1,-1))
        # vertical, horizontal, main diagonal and sec diagonal
        for dir in directions:
            result = 0
            result += self._checker(0, col, row, dir[0], dir[1], player)
            result += self._checker(0, col-dir[0], row-dir[1], -dir[0], -dir[1], player)
            # checks in a certain direction and in its opposite, if total consecutive piece number is >4 returns true
            # we do row and col -dir to avoid starting position being counted again
            if result >= 4: return True
        return False

    def _checker(self, count:int, col:int, row:int, col_step:int, row_step:int, player:int) -> int:
        # checks recursively how many elements are in a row from a certain position
        if col<0 or col>=self.cols or row<0 or row>=self.rows: return count   # reached edge of board
        if self.b[col][row] != player: return count    # reached empty or adversary position
        return self._checker(count+1, col+col_step, row+row_step, col_step, row_step, player) 

    def possible_states(self, curr_player: int)-> list:
        poss_states= []

        for col in range(self.cols):
            if self.heights[col]<self.rows: #verifica se é possível colocar mais uma peça na posição
                new_board= Board()

                for j in range(self.cols):  
                    new_board.heights[j]= self.heights[j]
                    for k in range(self.rows): new_board.b[j][k]= self.b[j][k]
                    
                new_board.drop(col, curr_player)
                poss_states.append(new_board)
                #print(new_board)
            
            if self.b[col][0]== curr_player:  # verifica se posso retirar
                new_board= Board()

                for j in range(self.cols):  
                    new_board.heights[j]= self.heights[j]
                    for k in range(self.rows): new_board.b[j][k]= self.b[j][k]                 

                new_board.pop(col)
                poss_states.append(new_board)
                #print(new_board)

        return poss_states


    #assumes that type is lowercase
    def is_valid_move(self, type, col, player):
        if (col<0 or col>=self.cols): return False
        if (type=="drop"):
            return (self.heights[col] < self.rows)
        elif (type=="pop"):
            return (self.b[col][0]==player)
        return False #o type nao é "drop" ou "pop"

            

    #assumes a valid move
    def apply_move(self, type, col, player):
        if (type=="drop"):
            self.drop(col, player)
        else: #type=="pop"
            self.pop(col)


if __name__ == "__main__":
    #so alguns testes:
    board_vertical_win = [
    ["X", "X", "X", "X", "-", "-"], # Col 0: X wins vertically here
    ["O", "O", "-", "-", "-", "-"], # Col 1
    ["O", "-", "-", "-", "-", "-"], # Col 2
    ["-", "-", "-", "-", "-", "-"], # Col 3
    ["-", "-", "-", "-", "-", "-"], # Col 4
    ["-", "-", "-", "-", "-", "-"], # Col 5
    ["-", "-", "-", "-", "-", "-"]  # Col 6
    ]
    board_horizontal_win = [
    ["X", "X", "-", "-", "-", "-"], # Col 0
    ["X", "-", "-", "-", "-", "-"], # Col 1
    ["O", "-", "-", "-", "-", "-"], # Col 2: O starts here
    ["O", "-", "-", "-", "-", "-"], # Col 3
    ["O", "X", "-", "-", "-", "-"], # Col 4
    ["O", "-", "-", "-", "-", "-"], # Col 5: O finishes here
    ["-", "-", "-", "-", "-", "-"]  # Col 6
    ]
    board_diag_positive = [
    ["-", "-", "-", "-", "-", "-"], # Col 0
    ["X", "-", "-", "-", "-", "-"], # Col 1: X at (1, 0)
    ["O", "X", "-", "-", "-", "-"], # Col 2: X at (2, 1)
    ["O", "O", "X", "-", "-", "-"], # Col 3: X at (3, 2)
    ["O", "X", "O", "X", "-", "-"], # Col 4: X at (4, 3)
    ["-", "-", "-", "-", "-", "-"], # Col 5
    ["-", "-", "-", "-", "-", "-"]  # Col 6
    ]
    board_diag_negative = [
    ["-", "-", "-", "-", "-", "-"], # Col 0
    ["-", "-", "-", "-", "-", "-"], # Col 1
    ["X", "X", "X", "O", "O", "-"], # Col 2: O at (2, 4)
    ["X", "X", "O", "O", "-", "-"], # Col 3: O at (3, 3)
    ["X", "O", "O", "-", "-", "-"], # Col 4: O at (4, 2)
    ["X", "O", "-", "-", "-", "-"], # Col 5: O at (5, 1)
    ["-", "-", "-", "-", "-", "-"]  # Col 6
    ]
    board_draw = [
    ["X", "X", "X", "O", "X", "X"], # Col 0
    ["O", "O", "X", "X", "O", "O"], # Col 1
    ["X", "X", "O", "O", "X", "X"], # Col 2
    ["O", "O", "X", "X", "O", "O"], # Col 3
    ["X", "X", "O", "O", "X", "X"], # Col 4
    ["O", "O", "X", "X", "O", "O"], # Col 5
    ["X", "X", "O", "O", "X", "X"]  # Col 6
    ]
    board_in_progress = [
    ["X", "-", "-", "-", "-", "-"], # Col 0
    ["O", "X", "-", "-", "-", "-"], # Col 1
    ["-", "-", "-", "-", "-", "-"], # Col 2
    ["O", "-", "-", "-", "-", "-"], # Col 3
    ["X", "O", "-", "-", "-", "-"], # Col 4
    ["-", "-", "-", "-", "-", "-"], # Col 5
    ["-", "-", "-", "-", "-", "-"]  # Col 6
    ]
    last_positions = [(0,-1), (3,-1), (2,-1), (5,-1), (4,-1), (0,-1)]
    # 1. Vertical Win
    heights_vertical_win = [4, 2, 1, 0, 0, 0, 0]
    # 2. Horizontal Win
    heights_horizontal_win = [2, 1, 1, 1, 2, 1, 0]
    # 3. Diagonal Win (Positive Slope)
    heights_diag_positive = [0, 1, 2, 3, 4, 0, 0]
    # 4. Diagonal Win (Negative Slope)
    heights_diag_negative = [0, 0, 5, 4, 3, 2, 0]
    # 5. Draw / Tie Game
    heights_draw = [6, 6, 6, 6, 6, 6, 6]
    # 6. Game in Progress
    heights_in_progress = [1, 2, 0, 1, 2, 0, 0]
    # Combined list of heights for iteration
    all_heights = [
        heights_vertical_win,
        heights_horizontal_win,
        heights_diag_positive,
        heights_diag_negative,
        heights_draw,
        heights_in_progress
    ]
    all_boards = [board_vertical_win, board_horizontal_win, board_diag_positive, board_diag_negative, board_draw, board_in_progress] 
    for i in range(6):
        teste = Board(board=all_boards[i])
        teste.last_move = last_positions[i]
        teste.heights = all_heights[i]
        print(teste)
        print(teste.isFinished())
        print("============================\n")

    #for i in range(3):
    #    teste.drop(1, "X")
    #print(teste)
    #for i in range(6):
    #    teste.pop(1)
    #print(teste)
