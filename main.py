from game.game import Game
from game.players import load_tree


def read_int(prompt):
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            return int(val)
        print("Invalid input. Please enter a valid number.")


ALGORITHMS = [
    ("MCTS Simplest",        "mcts_simplest"),
    ("MCTS Full",            "mcts_full"),
    ("MCTS New",             "mcts_new"),
    ("MCTS New Cycle",       "mcts_new_cycle"),
    ("MCTS Exp 1",           "mcts_new_exp1"),
    ("MCTS Exp 2",           "mcts_new_exp2"),
    ("Minimax (depth 3)",    "minimax"),
    ("Minimax (depth 4)",    "minimax4"),
    ("MCTS + Minimax",       "mcts_minimax"),
    ("ID3 Decision Tree",    None),
]

ID3_DEPTHS = [("None", None), ("5", 5), ("10", 10), ("20", 20), ("30", 30)]
ID3_SAMPLES = [1, 5, 10, 20, 50, 100]


def select_id3():
    print("\n--- ID3 Decision Tree ---")

    print("\nSelect max_depth:")
    for i, (label, _) in enumerate(ID3_DEPTHS, 1):
        print(f"  {i} - {label}")
    depth_choice = read_int("> ")
    while depth_choice < 1 or depth_choice > len(ID3_DEPTHS):
        depth_choice = read_int("Invalid option. Try again: ")
    depth = ID3_DEPTHS[depth_choice - 1][1]

    print("\nSelect min_samples:")
    for i, val in enumerate(ID3_SAMPLES, 1):
        print(f"  {i} - {val}")
    samples_choice = read_int("> ")
    while samples_choice < 1 or samples_choice > len(ID3_SAMPLES):
        samples_choice = read_int("Invalid option. Try again: ")
    samples = ID3_SAMPLES[samples_choice - 1]

    key = f"tree{depth}_{samples}"
    print(f"  -> {key}")
    load_tree(depth, samples)
    return key


def select_player(prompt):
    print(f"\n{prompt}")
    print("Select algorithm:")
    for i, (label, _) in enumerate(ALGORITHMS, 1):
        print(f"  {i} - {label}")
    choice = read_int("> ")
    while choice < 1 or choice > len(ALGORITHMS):
        choice = read_int("Invalid option. Try again: ")

    _, key = ALGORITHMS[choice - 1]
    if key is None:
        return select_id3()
    return key


def main():
    print("\nChoose game mode:")
    print("  1 - Human vs Human")
    print("  2 - Human vs Computer")
    print("  3 - Computer vs Computer")
    mode = read_int("> ")

    if mode == 1:
        Game("human", "human").run()

    elif mode == 2:
        p2 = select_player("Player 2 (Computer)")
        Game("human", p2).run()

    elif mode == 3:
        p1 = select_player("Player 1 (Computer)")
        p2 = select_player("Player 2 (Computer)")
        Game(p1, p2).run()


if __name__ == "__main__":
    main()
