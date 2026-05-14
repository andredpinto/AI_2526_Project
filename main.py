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
    if (mode==1):
        Game("human", "human").run()
    elif (mode==2):
        Game("human", "mcts_full").run()
    elif mode==3:
        Game("mcts_full", "mcts_full").run()
    elif mode==4:
        Game("human", "id3 in the nights").run()


if __name__=="__main__":
    main()
