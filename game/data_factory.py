import random
from game.board import Board
from game.players import MCTS

def generate_full_games(num_games, max_iter=1000):
    print("A gerar jogos MCTS vs MCTS")
    
    for i in range(num_games):
        b = Board()
        
        mcts_agent = MCTS(save_to_dataset=True, max_iter=max_iter)
        
        current_player = 1
        state_counts = {}
        
        while True:
            # MCTS faz a jogada
            mcts_agent.move(b, current_player)



            # verifica se alguem atingiu o criterio de vitoria ou derrota
            if b.isFinished(current_player):
                break
                
            # verifica se o jogo encravou
            if not b.possible_states(current_player * -1):
                break

            # previne loops infinitos
            key = b.hash_state(current_player * -1)
            state_counts[key] = state_counts.get(key, 0) + 1
            
            if state_counts[key] == 3:
                break # empate forçado
                
            if b.is_full():
                break

            current_player *= -1
            
        print(f"Jogo completo {i+1}/{num_games} terminado.")

def generate_random_states(num_states, max_iter=1000): 
    print("A gerar posicoes random para o MCTS resolver")
    
    for i in range(num_states):
        b = Board()
        
        # escolher um numero aleatorio de jogadas iniciais
        num_random_moves = random.randint(4, 25) # vão estar entre4 e 25 joagadas feitas anteriormente
        current_player = 1
        
        # fazer jogadas aleatorias
        for _ in range(num_random_moves):
            next_states = b.possible_states(current_player)
            if not next_states: 
                break
            b = random.choice(next_states) 
            current_player *= -1
            
        # verificar se alguem ja ganhou nestas jogadas à sorte, 
        # ou se o estado atual nao tem jogadas possiveis (empate)
        if b.isFinished(current_player * -1) or not b.possible_states(current_player):
            continue
            
        # o MCTS resolve este tabuleiro caótico
        mcts_agent = MCTS(save_to_dataset=True, max_iter=max_iter)
        mcts_agent.move(b, current_player)
        
        if (i+1) % 10 == 0:
            print(f"Estado aleatorio {i+1}/{num_states} resolvido e guardado.")

if __name__ == "__main__":
    # X jogos do inicio ao fim
    #generate_full_games(num_games=3) 
    
    # X situacoes estranhas a meio do jogo para o MCTS aprender
    generate_random_states(num_states=5000)
    
    print("Processo finalizado")