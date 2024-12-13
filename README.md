# Tic Tac Toe

This project implements an AI-powered Tic Tac Toe game using the Minimax algorithm. The AI is designed to play optimally, making it impossible to beat if both players play perfectly.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sandovaldavid/project0_tictactoe.git
   ```

2. Navigate to the project directory:

   ```bash
   cd project0_tictactoe
   ```

3. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To play the game, run the following command:

```bash
python runner.py
```

Follow the on-screen instructions to play against the AI.

## Project Structure

- `tictactoe.py`: Contains the main logic for the Tic Tac Toe game, including the Minimax algorithm implementation.
- `runner.py`: The entry point for running the game.
- `requirements.txt`: List of dependencies required for the project.

## How It Works

### Minimax Algorithm

The AI uses the Minimax algorithm to determine the optimal move. The algorithm works as follows:

1. **Player Function**: Determines which player's turn it is (X or O).
2. **Actions Function**: Returns all possible actions (moves) that can be taken on the board.
3. **Result Function**: Returns the board state after a move is made.
4. **Winner Function**: Determines if there is a winner on the board.
5. **Terminal Function**: Checks if the game is over.
6. **Utility Function**: Returns the utility of the board state (1 for X win, -1 for O win, 0 for tie).
7. **Minimax Function**: Recursively evaluates possible moves to find the optimal action.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to copy this content into a `README.md` file in your repository.
