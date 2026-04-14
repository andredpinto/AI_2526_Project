# metese aqui um dicionario ao que corresponde cada nome que se escolhe para jogar no main
# e dps as funcoes correspondentes
# TODO: mcts

def human_move(board, player):
    while (True):
        move= input("type collumn: ").lower().strip().split() #not case sensitive
        #o is_valid_move verifica por ele proprio se o user escreve drop ou pop
        #e vai verificar tbm se esta entre 0 e cols-1 ou 1 e cols
        #o que falta verificar é se so escreve duas coisas
        if (len(move)!=2):
            print("nono")
            continue
        type = move[0]
        col = int(move[1])-1
        if (board.is_valid_move(type, col, player)):
            #aplicar aqui diretamente ou so retorna?
            #como se vai treinar o mcts...? sera que com a  funcao do mcts faz mais sentido aplicar diretamente e nao retornar?
            board.apply_move(type, col, player)
            return



# the functions need to be declared beforehand
players = {
    "human" : human_move,
    #"ai" : anotherfunc
}
