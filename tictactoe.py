"""
Tic Tac Toe Player
"""

import math
import random
import json
import os

X = "X"
O = "O"
EMPTY = None

# Difficulty levels
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

# Theme options
THEME_CLASSIC = "classic"
THEME_DARK = "dark"
THEME_NEON = "neon"
THEME_RETRO = "retro"

# Piece options
PIECES_CLASSIC = "classic"  # X and O
PIECES_CUSTOM = "custom"    # Custom image icons

# Statistics file path
STATS_FILE = "game_stats.json"
# Settings file path
SETTINGS_FILE = "game_settings.json"

# Assets paths
ICONS_DIR = os.path.join("assets", "icons")
DEFAULT_X_ICON = os.path.join(ICONS_DIR, "x_icon.png")
DEFAULT_O_ICON = os.path.join(ICONS_DIR, "o_icon.png")

# Default settings
DEFAULT_SETTINGS = {
    "theme": THEME_CLASSIC,
    "pieces": PIECES_CLASSIC,
    "board_color": (255, 255, 255),
    "background_color": (0, 0, 0),
    "x_color": (255, 255, 255),
    "o_color": (255, 255, 255),
    "custom_x_icon": DEFAULT_X_ICON,
    "custom_o_icon": DEFAULT_O_ICON
}

# Theme color schemes
THEME_COLORS = {
    THEME_CLASSIC: {
        "board_color": (255, 255, 255),
        "background_color": (0, 0, 0),
        "x_color": (255, 255, 255),
        "o_color": (255, 255, 255),
        "highlight_color": (100, 100, 255)
    },
    THEME_DARK: {
        "board_color": (100, 100, 100),
        "background_color": (40, 40, 40),
        "x_color": (220, 220, 220),
        "o_color": (180, 180, 180),
        "highlight_color": (80, 180, 80)
    },
    THEME_NEON: {
        "board_color": (0, 255, 150),
        "background_color": (20, 20, 50),
        "x_color": (255, 50, 150),
        "o_color": (50, 200, 255),
        "highlight_color": (255, 255, 0)
    },
    THEME_RETRO: {
        "board_color": (210, 180, 140),
        "background_color": (50, 30, 0),
        "x_color": (200, 0, 0),
        "o_color": (0, 100, 200),
        "highlight_color": (255, 200, 0)
    }
}

# Piece symbols for different styles
PIECE_SYMBOLS = {
    PIECES_CLASSIC: {X: "X", O: "O"},
}

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # If X's count is equal to O's count, it's X's turn; otherwise, it's O's turn
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action: Cell is already occupied.")
    
    new_board = [row[:] for row in board]  # Deep copy of the board
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]
    
    # Check columns for a winner
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]
    
    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    
    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board) is not None:
        return True
    
    # Check if there are any empty cells
    for row in board:
        if EMPTY in row:
            return False
    
    # If no empty cells and no winner, it's a tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board, difficulty=HARD):
    """
    Returns the optimal action for the current player on the board based on difficulty level.
    """
    if terminal(board):
        return None
    
    possible_actions = list(actions(board))
    
    # Easy difficulty: Random moves
    if difficulty == EASY:
        return random.choice(possible_actions)
    
    # Medium difficulty: 50% chance of making the optimal move, 50% chance of a random move
    elif difficulty == MEDIUM:
        if random.random() < 0.5:
            return random.choice(possible_actions)
    
    # For HARD difficulty or the 50% of MEDIUM where we make optimal moves
    def max_value(board, depth=0):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action), depth + 1))
        return v

    def min_value(board, depth=0):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action), depth + 1))
        return v

    current_player = player(board)
    if current_player == X:
        best_val = -math.inf
        best_action = None
        for action in possible_actions:
            action_val = min_value(result(board, action))
            if action_val > best_val:
                best_val = action_val
                best_action = action
    else:
        best_val = math.inf
        best_action = None
        for action in possible_actions:
            action_val = max_value(result(board, action))
            if action_val < best_val:
                best_val = action_val
                best_action = action
    
    return best_action


def load_stats():
    """
    Load game statistics from file or create default stats if file doesn't exist.
    """
    default_stats = {
        "games_played": 0,
        "player_wins": 0,
        "ai_wins": 0,
        "ties": 0,
        "by_difficulty": {
            EASY: {"games": 0, "player_wins": 0, "ai_wins": 0, "ties": 0},
            MEDIUM: {"games": 0, "player_wins": 0, "ai_wins": 0, "ties": 0},
            HARD: {"games": 0, "player_wins": 0, "ai_wins": 0, "ties": 0}
        }
    }
    
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
            return stats
        except (json.JSONDecodeError, IOError):
            return default_stats
    else:
        return default_stats


def save_stats(stats):
    """
    Save game statistics to file.
    """
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=4)
        return True
    except IOError:
        return False


def update_stats(player_symbol, winner, difficulty):
    """
    Update game statistics after a game ends.
    
    Args:
        player_symbol: The symbol (X or O) the human player was using
        winner: The winner of the game (X, O, or None for a tie)
        difficulty: The difficulty level used for the game
    """
    stats = load_stats()
    
    # Update overall game count
    stats["games_played"] += 1
    
    # Update by difficulty
    stats["by_difficulty"][difficulty]["games"] += 1
    
    # Update win/loss/tie stats
    if winner is None:
        # It's a tie
        stats["ties"] += 1
        stats["by_difficulty"][difficulty]["ties"] += 1
    elif winner == player_symbol:
        # Player won
        stats["player_wins"] += 1
        stats["by_difficulty"][difficulty]["player_wins"] += 1
    else:
        # AI won
        stats["ai_wins"] += 1
        stats["by_difficulty"][difficulty]["ai_wins"] += 1
    
    save_stats(stats)
    return stats


def load_settings():
    """
    Load game settings from file or create default settings if file doesn't exist.
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            return settings
        except (json.JSONDecodeError, IOError):
            return DEFAULT_SETTINGS
    else:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS


def save_settings(settings):
    """
    Save game settings to file.
    """
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        return True
    except IOError:
        return False


def get_piece_symbol(piece, piece_style=PIECES_CLASSIC):
    """
    Get the symbol for a piece based on the selected style.
    """
    if piece == EMPTY:
        return ""
    return PIECE_SYMBOLS.get(piece_style, PIECE_SYMBOLS[PIECES_CLASSIC])[piece]


def get_theme_colors(theme=THEME_CLASSIC):
    """
    Get the color scheme for a theme.
    """
    return THEME_COLORS.get(theme, THEME_COLORS[THEME_CLASSIC])
