# AGENTS.md

## Running the Project

- **Run Connect4 game**: `python main.py` (interactive menu: Human vs Human, Human vs AI, AI vs AI)
- **No test framework** - no pytest/unittest exists; don't search for test commands

## Project Structure

- `main.py` → Entry point for Connect4 game
- `game.py`, `board.py`, `players.py` → Connect4 game logic
- `decision_tree/` → ID3 decision tree module (placeholder code, incomplete)
- `data/iris.csv` → Sample dataset for decision tree testing

## Notes

- No lint/typecheck/formatting config (black, ruff, mypy not set up)
- Python environment uses Conda (see `.vscode/settings.json`)
- Game uses standard library only (no external dependencies)