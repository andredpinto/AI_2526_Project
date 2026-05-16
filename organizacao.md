organizacao:
main.py é o que se corre para jogar o jogo, permite escolher o modo.

o modo é escolhido com base em strings que sao as chaves num dicionario mapeadas para funcoes que fazem as jogadas. Isto vai estar no ficheiro players.py

O estado do jogo em si vai estar em game.py e suponho que podemos meter aqui um metodo que comunica com tudo e que corre o jogo
e depois o tabuleiro com as x funcoes que precisamos em board.py

uma possivel mudanca é criar uma pasta dentro de game/, por exemplo ai/
e o players.py ficava só com o dicionario

eu sei que está a ficar um pouco confuso o qeu se tá a passar com os mcts:

**o que se fez primeiro:**
- usava-se em todo o algoritmo do mcts uma lista de estados possiveis, ineficiente
- regras(policies) para contorlar que estados se explorava durante a simulação, só que isto é muito ineficiente

**o que se esta a modificar:**
- usar uma lista de moves quando possivel
- criar regras para so expandir nós (em vez de fazer isso na simulacao) ->bons resultados e rapido
- criar um minimax, para substituir a simulacao do monte carlo
- criar heuristicas que se podem usar em diferentes sitios
- (regras e heuristicas para o minimax e expansao de nós estou a colocar em *utils.py*)

**o que ainda pode confundir e não me apetece mexer:**
- o que se usa durante a simulação não é bem uma heuristica como as que tou a criar agora -> usar palavras diferentes?- usar simulation_policies como se fez para a expansao
- mcts original em players.py e o novo mcts melhor está em mcts_moves.py -> melhorar a organização?
- limpar alguns comentários e melhorar a escrita?