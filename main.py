from game import Game

#cada player é identificado por uma string
# essa string esta num dicionario em player.py e faz corresponder a uma funcao para fazer a jogada
def main():
    print("Choose game mode:")
    print("1 - Human vs Human")
    mode = int(input().strip())
    if (mode==1):
        Game("human", "human").run()
    # else if (mode==2):
    #
    # else if mode==3:


if __name__=="__main__":
    main()
