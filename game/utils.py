from game.board import Board
#=============Expansion policies==========================
#returns all possible moves
def get_all_moves(board:Board, player):
    return board.possible_moves(player)

def get_win_or_all(board:Board, player):
    moves = board.possible_moves(player)
    winning_moves = []

    for move in moves:
        test_board = board.copy()
        test_board.apply_move(move[0], move[1], player)

        if test_board.winner(player) == player:
            winning_moves.append(move)

    return winning_moves if winning_moves else moves

#only returns moves that the opponent doesnt win right after
#very similar to the block_win in the simulation policy
def get_block_or_all(board: Board, player):
    moves = board.possible_moves(player)
    good_moves = []

    for move in moves:
        test_board = board.copy()
        test_board.apply_move(move[0], move[1], player)

        if test_board.winner(player) == -player:
            continue

        opponent_can_win = False

        for opp_move in test_board.possible_moves(-player):
            opp_board = test_board.copy()
            opp_board.apply_move(opp_move[0], opp_move[1], -player)

            if opp_board.winner(-player) == -player:
                opponent_can_win = True
                break

        if not opponent_can_win:
            good_moves.append(move)

    return good_moves if good_moves else moves

#could make it more efficient but whatever
def get_win_block_or_all(board: Board, player):
    moves = board.possible_moves(player)

    win_moves = get_win_or_all(board, player)
    if win_moves != moves:
        return win_moves

    return get_block_or_all(board, player)

#=======================HEURISTICS:=================================
#the scores will be between [-1,1] para este novo mcts não dar mais importância ao componente de exploitation do qeu os outros, isto seria uma fator a ter em consideração separadamente
#i'm thinking about modularity in the heuristics and then aggregating them... the final result should be inside [-1,1]

def heuristic_win(board:Board, player): #the player is only for the draw check, tells who is playing
    """returns the winner(-1 or 1), 0 for draw or if there's no winner"""
    winner = board.winner(player)
    if (winner != None):
        return winner #0 -1 or 1, 0 for draw
    return 0

def heuristic_threat_3(board:Board):
    """if there exists a threat (3x in a "row") it returns a higher aboslute value\n
    this should be used only after the heuristic_win returns 1/-1, because this heuristic returns 0.3 even if it finds a win\n
    example: if player==-1 and he has three pieces next to each other ->returns -0.3
    """
    for col in range(board.cols):
        for row in range(board.rows):
            if (board.b[col][row]!=0):
                if board._pos_checker(col, row, threat=True): #i think this won't break anything
                    return 0.3*board.b[col][row]
    return 0

def heuristic_next_move_win(board, player): #player because it depends on who can play (pop)
    """if there's any move that leads to a win"""
    for move in board.possible_moves(player):
        b = board.copy()
        b.apply_move(move[0], move[1], player)
        if b.winner(player) == player:
            return 1*player
    return 0

def heuristic_center_control(board, multiplier=0.01):#não sei por quanto multiplicar
    weights = [1, 2, 3, 4, 3, 2, 1] #weights for each col
    score = 0
    for col in range(board.cols):
        for row in range(board.rows):
            score += board.b[col][row] * weights[col]
    return multiplier*score
#TODO create a new function for finding the threats instead of using _pos_checker 
#se calhar nao implemento o resto, não estou a ver uma maneira rapida e facil de fazer isto e estamos a ficar sem tempo
def heuristic_threat_2(board):
    """2 pieces together, maybe multiply by a counter"""
def heuristic_threat_3_open_ends(board):
    """if there's a threat with 2 open ends (like: -XXX--) it's probably a win, not guaranteed because pop"""
#não tenho mais ideias por agora, ficamos por aqui, fica a ideia qeu isto pode ser muito melhor com melhores heurisitcask
def clamp(score):
    return max(-1, min(1, score))

def heuristic1(board, player):
    """win + threat_3"""
    return clamp(
        heuristic_win(board, player)
        + heuristic_threat_3(board)
    )

def heuristic2(board, player):
    """win + threat_3 + center"""
    return clamp(
        heuristic_win(board, player)
        + heuristic_threat_3(board)
        + heuristic_center_control(board)
    )

def heuristic3(board, player):
    """win + next_move_win + threat_3 + center"""
    return clamp(
        heuristic_win(board, player)
        + heuristic_next_move_win(board, player)
        + heuristic_threat_3(board)
        + heuristic_center_control(board)
    )