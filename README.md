# AI 2025/2026 — PopOut Connect Four

Projeto desenvolvido no âmbito da unidade curricular de Inteligência Artificial da FCUP.

## Elementos do grupo

- André Pinto
- Maiara Guedes
- João Azevedo

## Descrição

Este projeto implementa o jogo **PopOut Connect Four**, uma variante do Connect Four em que cada jogador pode:

- fazer `drop` de uma peça numa coluna, como no Connect Four clássico;
- fazer `pop` numa coluna, removendo a sua peça da base dessa coluna.

Além do modo humano, foram implementados e comparados vários agentes de IA:

- MCTS original, baseado em estados;
- MCTS novo, baseado em movimentos;
- Minimax com poda alfa-beta;
- MCTS híbrido com avaliação Minimax;
- árvores de decisão ID3 treinadas a partir de dados gerados por MCTS.

## Como correr

Na raiz do projeto:

```bash
python main.py
```

O menu permite escolher:

1. Human vs Human
2. Human vs Computer
3. Computer vs Computer

Quando um humano joga, o movimento deve ser introduzido no formato:

```text
drop 4
pop 3
```

As colunas são numeradas de 1 a 7.

## Organização do projeto

```text
.
├── main.py
├── game/
│   ├── board.py
│   ├── game.py
│   ├── players.py
│   ├── mcts_moves.py
│   ├── minimax.py
│   ├── utils.py
│   ├── data_storage.py
│   └── data_factory.py
├── decision_tree/
│   ├── id3.py
│   ├── node.py
│   ├── metrics.py
│   ├── auxiliar.py
│   └── pre_trained_trees/
├── data/
│   ├── dataset_mcts.csv
│   └── iris.csv
├── notebooks/
│   ├── analysis_mcts.ipynb
│   └── analysis_id3.ipynb
└── scripts/
    ├── train_id3.py
    └── load_id3_test.py
```

### `main.py`

Ponto de entrada do projeto. Mostra o menu interativo, permite escolher o modo de jogo e seleciona os agentes usados em cada partida.

### `game/`

Contém a lógica principal do jogo e dos agentes.

- `board.py` define o tabuleiro, movimentos válidos, aplicação de `drop`/`pop`, deteção de vencedor, empates e cópia de estados.
- `game.py` gere o ciclo de jogo, alternância de jogadores, regras adicionais de empate e recolha de estatísticas para os notebooks.
- `players.py` liga nomes de agentes a funções de jogada através do dicionário `players`. Também contém a primeira versão do MCTS.
- `mcts_moves.py` contém a versão nova do MCTS, baseada em movimentos em vez de estados completos.
- `minimax.py` contém o agente Minimax com poda alfa-beta.
- `utils.py` contém políticas de expansão e heurísticas usadas pelo MCTS e pelo Minimax.
- `data_storage.py` guarda estados e jogadas num dataset para treino das árvores de decisão.
- `data_factory.py` gera dados automaticamente a partir de jogos ou estados resolvidos por MCTS.

### `decision_tree/`

Contém a implementação do ID3.

- `id3.py` implementa treino, previsão e previsão restringida a jogadas válidas.
- `node.py` define os nós da árvore de decisão.
- `metrics.py` implementa entropia e ganho de informação.
- `auxiliar.py` contém funções auxiliares para validação, divisão de datasets e cálculo de maiorias.
- `pre_trained_trees/` contém árvores ID3 já treinadas, usadas no menu principal.

### `data/`

Contém datasets usados no projeto.

- `dataset_mcts.csv` contém estados de jogo e jogadas escolhidas por MCTS, usado para treinar o ID3.
- `iris.csv` é um dataset simples usado para testar a implementação genérica do ID3.

### `notebooks/`

Contém a análise experimental.

- `analysis_mcts.ipynb` compara as variantes de MCTS, Minimax e MCTS híbrido.
- `analysis_id3.ipynb` analisa a árvore de decisão ID3.

### `scripts/`

Contém scripts auxiliares.

- `train_id3.py` treina várias árvores ID3 com diferentes valores de `max_depth` e `min_samples`.
- `load_id3_test.py` foi usado para testes de carregamento de árvores.

## Agentes disponíveis no menu

Os agentes disponíveis são definidos em `game/players.py`:

- `human`: jogador humano.
- `mcts_simplest`: MCTS original com limite de filhos.
- `mcts_full`: MCTS original com heurísticas de simulação e reutilização da árvore.
- `mcts_new`: versão nova do MCTS baseada em movimentos.
- `mcts_new_cycle`: variante do MCTS novo com deteção de ciclos nos rollouts.
- `mcts_new_exp1`: variante experimental com política de expansão `get_win_or_all`.
- `mcts_new_exp2`: variante experimental com política de expansão `get_win_block_or_all`.
- `minimax`: Minimax com profundidade 3.
- `minimax4`: Minimax com profundidade 4.
- `mcts_minimax`: MCTS híbrido que substitui o rollout por avaliação Minimax.
- `tree{depth}_{min_samples}`: árvores ID3 pré-treinadas, por exemplo `tree30_20`.

## Regras e detalhes de implementação

- O tabuleiro usa valores `1`, `-1` e `0` para representar os dois jogadores e casas vazias.
- Se um `pop` criar quatro em linha para ambos os jogadores, ganha o jogador que fez o `pop`.
- Se um `pop` criar vitória apenas para o adversário, o jogador que fez o `pop` perde.
- O estado do tabuleiro inclui também o jogador que vai jogar, para distinguir posições iguais com turnos diferentes.
- Existem regras adicionais para evitar jogos infinitos, como deteção de estados repetidos e possibilidade de empate quando o tabuleiro está cheio.

## Resumo dos algoritmos

### MCTS original

A primeira versão está em `game/players.py`. Cada nó guarda estados completos possíveis. Durante a expansão e simulação, são criados novos tabuleiros completos, o que torna esta versão mais pesada.

### MoveMCTS

A versão nova está em `game/mcts_moves.py`. Em vez de guardar diretamente estados completos por expandir, guarda movimentos possíveis. O tabuleiro só é copiado quando o movimento é efetivamente expandido. Esta alteração reduz o custo de cópias e permite usar mais iterações.

### Políticas de expansão

As políticas estão em `game/utils.py`:

- `get_all_moves`: expande todos os movimentos válidos.
- `get_win_or_all`: se existir uma jogada vencedora imediata, expande apenas essa; caso contrário, expande todas.
- `get_win_block_or_all`: prioriza vitórias imediatas e tenta evitar movimentos que dão vitória imediata ao adversário.

### Minimax

O Minimax está em `game/minimax.py` e usa poda alfa-beta. As heurísticas principais estão em `game/utils.py`:

- `heuristic_win`
- `heuristic1`
- `heuristic2`
- `heuristic3`

A profundidade prática é limitada pelo fator de ramificação do PopOut, que pode chegar a 14 movimentos por turno.

### ID3

O ID3 foi implementado em `decision_tree/` e treinado com dados gerados a partir de decisões do MCTS. No jogo, as árvores carregadas escolhem uma jogada entre as jogadas válidas para o estado atual.

## Treinar árvores ID3

Para treinar novamente as árvores ID3, correr a partir da raiz do projeto:

```bash
python scripts/train_id3.py
```

O script usa `data/dataset_mcts.csv` e guarda os modelos em:

```text
decision_tree/pre_trained_trees/
```

## Notas

- O jogo principal deve ser corrido a partir da raiz do projeto, porque os caminhos para as árvores pré-treinadas são relativos a essa diretoria.
- O projeto não tem uma framework de testes configurada.
- Os notebooks guardam os resultados usados na análise, mas devido à aleatoriedade do MCTS os valores podem variar entre execuções.
