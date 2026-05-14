#TODO validar se a jogada é legal no proprio metodo(pop e drop) ou fora
class Board: #tabuleiro de connect4 com var. de dar pop out
    #possiveis otimizacoes:
        # usar numpy arrays?
    def __init__(self, rows=6, cols=7, board=None): #wtf is this board=None this doesnt make any sense i have no idea why i did this ??? im not oging to delete in case im using it somewhere i think im going to use it actually hahah attention to update the other attributes
        self.rows = rows
        self.cols = cols
        self.heights = [0] * cols
        if board==None:
            self.b = [[0 ] * rows for _ in range(cols)] # cada lista é uma coluna, por tanto primeiro acedemos as colunas e dps às linhas
        else: self.b = board
        self.last_move = (-1, -1) #(col, row) quando se faz pop, o valor da linha fica -1
        self.last_player = None

    def drop(self, col, player:int): # col toma valores de 0 a cols-1(6)
        h = self.heights[col]
        self.b[col][h] = player
        self.last_move = (col, h)
        self.last_player = player
        self.heights[col] += 1

    def pop(self, col, player):
        for i in range(self.heights[col]-1):
            self.b[col][i] = self.b[col][i+1]
        self.b[col][self.heights[col]-1] = 0 #para nao aceder a zonas inexistentes no array
        self.heights[col] -=1
        self.last_player = player
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
    
    def isFinished(self, player) -> bool:
        return self.winner(player) is not None

    #retorna 0 se for empate e none se ainda nao tiver acabado
    def winner(self, player):
        if self.last_move[0]==-1: return None  # No plays yet; change this if initialization is changed
        col = self.last_move[0]
        row = self.last_move[1]
        if row != -1:    # last move was an insertion, safe to check only the insertion spot
            if self._pos_checker(col, row): #4 in a row detected
                return self.b[col][row]

        else:   # check all of the rows in the col
            players_won = set() # set para a 1 regra adicional, se houver 2 winners por causa do pop: ganha o que fez o pop
            for i in range(self.heights[col]):
                if self._pos_checker(col, i): 
                    players_won.add(self.b[col][i])
            if len(players_won)==1: return players_won.pop()
            if len(players_won)==2: return self.last_player

        if self._is_draw(player):
            return 0

        return None
    
    #cada estado para ser unico precisa de o player a jogar e do tabuleiro
    #o python nao deixa uma lista tar na chave pq é mutavel entao preciso de converter para tuplo
    def hash_state(self, player):
        return (player, tuple(tuple(col) for col in self.b))

    #eu tenho de percorrer todas as colunas e ver se ha movimentos validos
    #a maneira mais direta era reutilizar a funcao do possible_states mas pareceme menos eficiente
    def _is_draw(self, player):
        for col in range(self.cols):
            if self.is_valid_move("drop", col, player):
                return False
            if self.is_valid_move("pop", col, player):
                return False
        return True
    
    #util para regra adicional 2
    def is_full(self):
        for h in self.heights:
            if h < self.rows:
                return False
        return True

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

    #isto retorna estados terminais de proposito
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
            
            if self.b[col][0]== curr_player:  # verifica se posso retirar
                new_board= Board()

                for j in range(self.cols):  
                    new_board.heights[j]= self.heights[j]
                    for k in range(self.rows): new_board.b[j][k]= self.b[j][k]                 

                new_board.pop(col, curr_player)
                poss_states.append(new_board)

        return poss_states
    
    def possible_moves(self, curr_player:int)->list:
        """returns a list with tuples like ("drop", 1)"""
        poss_moves= []
        for col in range(self.cols):
            if self.heights[col]<self.rows: #verifica se é possível colocar mais uma peça na posição
                poss_moves.append(("drop"), col)
            
            if self.b[col][0]== curr_player:  # verifica se posso retirar
                poss_moves.append(("pop", col))

        return poss_moves
    
    def copy(self):
        new_board = []
        for col in self.b:
            new_board.append(col.copy())

        b_copy = Board(board=new_board)
        b_copy.heights = self.heights.copy()
        b_copy.last_move = self.last_move
        b_copy.last_player =self.last_player

        return b_copy

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
            self.pop(col, player)
