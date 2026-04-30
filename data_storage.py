import csv
import os

move_dict = {
    "drop_1": 0, "drop_2": 1, "drop_3": 2, "drop_4": 3, "drop_5": 4, "drop_6": 5, "drop_7": 6,
    "pop_1": 7,  "pop_2": 8,  "pop_3": 9,  "pop_4": 10, "pop_5": 11, "pop_6": 12, "pop_7": 13
}

#para saber se ja guardamos um estado igual antes, para evitar duplicados no dataset
estados_guardados = set()

def save_to_dataset(board, player, move, filename="dataset_mcts.csv"):
   
    # verifica se ja vimos este tabuleiro
    estado_hash = board.hash_state(player)
    if estado_hash in estados_guardados:
        return
        
    estados_guardados.add(estado_hash)

    # transforma o tabuleiro numa lista com uma dimensao
    flat_board = []
    for col in board.b:
        for piece in col:
            # multiplica pelo player para que o 1 represente sempre a peca de quem joga
            flat_board.append(piece * player) 
            
    # formata a jogada (drop, 0) -> drop_1 para procurar no dicionário
    form_move = f"{move[0]}_{move[1] + 1}"
    numeric_move = move_dict[form_move]
    
    file_exists = os.path.isfile(filename)
    
    # guarda no ficheiro CSV
    with open(filename, mode='a', newline='') as file: #mode a para "append", newline='' evita linhas em branco extra
        writer = csv.writer(file)
        
        # se o ficheiro for novo, escreve o cabecalho primeiro
        if not file_exists:
            header = [f"pos_{i}" for i in range(42)] + ["move"]
            writer.writerow(header)
            
        # escreve a linha com o estado atual e a jogada escolhida (num)
        writer.writerow(flat_board + [numeric_move])