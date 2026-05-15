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
#a escala/ os valores que as heuristicas é algo que terei que definir depois
#i'm thinking about modularity in the heuristics and then aggregating them...
def heuristic_win(board:Board, player):
    ...

def heuristic_threat(board:Board, player):
    """if there exists a threat (3x in a "row") it returns a higher aboslute value\n
    for example if player -1 has a 3 in a row it will return -100 while if it was player 1 it would be 100 """
    ...