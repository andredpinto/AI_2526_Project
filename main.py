from game.game import Game

#cada player é identificado por uma string
# essa string esta num dicionario em player.py e faz corresponder a uma funcao para fazer a jogada
def main():
    print("Choose game mode:")
    print("1 - Human vs Human")
    print("2 - Human vs MCTS")
    print("3 - MCTS vs MCTS")
    print("4 - Human vs Tree in the nights")

    mode = int(input().strip())

    if mode == 1:
        Game("human", "human").run()

    elif mode == 2:
        Game("human", "mcts_new").run()

    elif mode == 3:
        Game("mcts_new", "mcts_new").run()

    elif mode == 4:
        Game("human", "id3 in the nights").run()

    # hidden/experimental modes
    elif mode == 5:
        Game("human", "mcts_full").run()

    elif mode == 6:
        Game(player1="mcts_new_exp1", player2="mcts_new_exp2").run()

    elif mode == 7:
        Game(player1="minimax4", player2="mcts_new").run()

    elif mode == 8:
        Game(player1="mcts_minimax", player2="mcts_new").run()

    elif mode == 9:
        Game("human", "mcts_new_cycle").run()
    
    elif mode == 10:
        Game("human", "tree20_10").run()

if __name__=="__main__":
    main()
