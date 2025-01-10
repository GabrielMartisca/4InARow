import random

class Connect4:
    """
      Class to represent the 4 in a row/connect4 game.
       Attributes:  
           rows: Number of rows in the board
            cols: Number of columns in the board
            board: 2D list to represent the board
            current_player: Player who has the current turn
            players: Dictionary to store the types of players
            BOT_PIECE: Piece used to represent the bot
            PLAYER_PIECE: Piece used to represent the player
            EMPTY: Piece used to represent an empty cell
            ROW_COUNT: Number of rows in the board
            COLUMN_COUNT: Number of columns in the board
            WINDOW_LENGTH: Number of consecutive pieces required to win
        Methods:
            make_move: Function to make a move in the game
            is_valid_move: Function to check if a move is valid
            is_terminal_node: Function to check if the game has ended
            winning_move: Function to check if a player has won
            get_next_open_row: Function to get the next open row in a column
            drop_piece: Function to drop a piece in a column
            check_winner: Function to check if a player has won
            check_draw: Function to check if the game is a draw
            switch_player: Function to switch the current player
            reset_game: Function to reset the game
            get_board_state: Function to get the current board state
            get_valid_locations: Function to get the valid locations to make a move
            minimax: Function to implement the minimax algorithm
            score_position: Function to score the current position
            evaluate_window: Function to evaluate a window of pieces
            get_ai_move: Function to get the move for the AI

   
    
       """
    def __init__(self, rows=6, cols=7, p1="human", p2="human"):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_player = 1
        self.players = {1: p1, 2: p2}
        self.BOT_PIECE = 2
        self.PLAYER_PIECE = 1
        self.EMPTY = 0
        self.ROW_COUNT = rows
        self.COLUMN_COUNT = cols
        self.WINDOW_LENGTH = 4

    def make_move(self, col):
        """
    Make a move in the specified column.

    This method places the current player's piece in the specified column.
    It searches from the bottom of the column upwards to find the first empty slot.
    If a move is made, it returns the row and column of the placed piece.
    If the column is full, it returns None.

    Args:
        col (int): The column where the current player wants to place their piece.

    Returns:
        tuple: A tuple (row, col) indicating the position of the placed piece,
               or None if the column is full.
    """
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return row, col
        return None

    def is_valid_move(self, col):
        """
    Check if a move is valid in the specified column.

    This method checks if the topmost slot in the specified column is empty,
    indicating that a piece can be placed in that column.

    Args:
        col (int): The column to check for a valid move.

    Returns:
        bool: True if the column has at least one empty slot, False otherwise.
    """
        return self.board[0][col] == 0

    def is_terminal_node(self, board):
        """
    Check if the current board state is a terminal node.

    This method checks if the current board state is a terminal node,
    which means the game has ended. The game can end if either player has won
    or if the board is full, resulting in a draw.

    Args:
        board (list): The current state of the game board.

    Returns:
        bool: True if the game has ended (either player has won or it's a draw),
              False otherwise.
    """
        return self.winning_move(board, self.BOT_PIECE) or self.winning_move(board, self.PLAYER_PIECE) or self.check_draw()

    def winning_move(self, board, piece):
        """
    Check if the specified piece has a winning move on the board.

    This method checks if the specified piece has four consecutive pieces
    in a row, either horizontally, vertically, or diagonally.

    Args:
        board (list): The current state of the game board.
        piece (int): The piece to check for a winning move (e.g., BOT_PIECE or PLAYER_PIECE).

    Returns:
        bool: True if the specified piece has a winning move, False otherwise.
    """
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True
        return False

    def get_next_open_row(self, board, col):
        """
    Get the next open row in the specified column.

    This method searches from the bottom of the specified column upwards
    to find the first empty slot.

    Args:
        board (list): The current state of the game board.
        col (int): The column to search for an open row.

    Returns:
        int: The row index of the first empty slot in the specified column,
             or None if the column is full.
    """
        for r in range(self.ROW_COUNT - 1, -1, -1):
            if board[r][col] == 0:  
                return r
        return None  


    def drop_piece(self, board, row, col, piece):
        """
    Drop a piece into the specified position on the board.

    This method places the specified piece in the given row and column
    on the board.

    Args:
        board (list): The current state of the game board.
        row (int): The row index where the piece should be placed.
        col (int): The column index where the piece should be placed.
        piece (int): The piece to place on the board (e.g., BOT_PIECE or PLAYER_PIECE).

    Returns:
        None
    """
        board[row][col] = piece

    def check_winner(self, row, col, player):
        """
    Check if the specified player has won the game.

    This method checks if the specified player has four consecutive pieces
    in a row, either horizontally, vertically, or diagonally, starting from
    the given position.

    Args:
        row (int): The row index of the starting position.
        col (int): The column index of the starting position.
        player (int): The player to check for a winning move.

    Returns:
        bool: True if the specified player has won, False otherwise.
    """
        def count_consecutive_tokens(dr, dc):
            """
    Count consecutive tokens in a specified direction.

    This helper method counts the number of consecutive tokens for the current player
    starting from a given position and moving in the specified direction.

    Args:
        dr (int): The row direction to move (e.g., 1 for down, -1 for up, 0 for no vertical movement).
        dc (int): The column direction to move (e.g., 1 for right, -1 for left, 0 for no horizontal movement).

    Returns:
        int: The number of consecutive tokens in the specified direction.
    """
            count = 0
            r, c = row, col
            while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            return count - 1

        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            if count_consecutive_tokens(dr, dc) + count_consecutive_tokens(-dr, -dc) >= 3:
                return True
        return False

    def check_draw(self):
        """
    Check if the game is a draw.

    This method checks if the game board is full and no more valid moves can be made,
    indicating that the game has ended in a draw.

    Returns:
        bool: True if the game is a draw (no valid moves left), False otherwise.
    """
        for col in range(self.cols):
            if self.is_valid_move(col):
                return False
        return True

    def switch_player(self):
        """
    Switch the current player.

    This method switches the current player from player 1 to player 2 or from player 2 to player 1.
    It uses the fact that the sum of player 1 and player 2 is 3 to toggle between the two players.

    Returns:
        None
    """
        self.current_player = 3 - self.current_player

    def reset_game(self):
        """
    Reset the game to its initial state.

    This method clears the game board and sets the current player to player 1,
    effectively restarting the game.

    Returns:
        None
    """
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1


    def get_board_state(self):
        """
    Get the current state of the game board.

    This method returns the current state of the game board as a list of lists.

    Returns:
        list: The current state of the game board.
    """
        return self.board

    def get_valid_locations(self, board):
        """
    Get a list of valid column indices where a move can be made.

    This method returns a list of column indices that have at least one empty slot,
    indicating that a move can be made in those columns.

    Args:
        board (list): The current state of the game board.

    Returns:
        list: A list of column indices where a move can be made.
    """
        return [col for col in range(self.COLUMN_COUNT) if self.is_valid_move(col)]

    def minimax(self, board, depth, alpha, beta, maximisingPlayer):
        """
    Perform the Minimax algorithm with alpha-beta pruning to determine the best move.

    This method uses the Minimax algorithm with alpha-beta pruning to evaluate the game tree
    and determine the best move for the current player. It recursively explores possible moves
    to a specified depth and evaluates the board state to find the optimal move.

    Args:
        board (list): The current state of the game board.
        depth (int): The maximum depth to explore in the game tree.
        alpha (float): The best value that the maximising player can guarantee.
        beta (float): The best value that the minimising player can guarantee.
        maximisingPlayer (bool): True if the current player is the maximising player, False otherwise.

    Returns:
        tuple: A tuple (column, value) where 'column' is the best column to play and 'value' is the evaluation score.
    """
        valid_locations = self.get_valid_locations(board)

        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.BOT_PIECE):
                    return (None, 9999999)
                elif self.winning_move(board, self.PLAYER_PIECE):
                    return (None, -9999999)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, self.BOT_PIECE))

        if maximisingPlayer:
            value = -9999999
            column = random.choice(valid_locations)  
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                if row is not None:  
                    b_copy = [row[:] for row in board]  
                    self.drop_piece(b_copy, row, col, self.BOT_PIECE)
                    new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return column, value

        else:  
            value = 9999999
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                if row is not None: 
                    b_copy = [row[:] for row in board]
                    self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                    new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return column, value


    def score_position(self, board, piece):
        """
    Evaluate the board and return a score for the specified piece.

    This method evaluates the current state of the game board and calculates a score
    for the specified piece based on its positions. The score is calculated by
    considering the number of pieces in the center column, horizontal, vertical,
    and diagonal windows.

    Args:
        board (list): The current state of the game board.
        piece (int): The piece to evaluate the score for (e.g., BOT_PIECE or PLAYER_PIECE).

    Returns:
        int: The calculated score for the specified piece.
    """
        score = 0

        centre_array = [board[r][self.COLUMN_COUNT // 2] for r in range(self.ROW_COUNT)]
        centre_count = centre_array.count(piece)
        score += centre_count * 3

        for r in range(self.ROW_COUNT):
            row_array = board[r]
            for c in range(self.COLUMN_COUNT - self.WINDOW_LENGTH + 1):
                window = row_array[c:c + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for c in range(self.COLUMN_COUNT):
            col_array = [board[r][c] for r in range(self.ROW_COUNT)]
            for r in range(self.ROW_COUNT - self.WINDOW_LENGTH + 1):
                window = col_array[r:r + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT - self.WINDOW_LENGTH + 1):
            for c in range(self.COLUMN_COUNT - self.WINDOW_LENGTH + 1):
                window = [board[r + i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT - self.WINDOW_LENGTH + 1):
            for c in range(self.COLUMN_COUNT - self.WINDOW_LENGTH + 1):
                window = [board[r + self.WINDOW_LENGTH - 1 - i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score


    def evaluate_window(self, window, piece):
        """
    Evaluate a window of four consecutive slots and return a score for the specified piece.

    This method evaluates a window of four consecutive slots on the board and calculates a score
    for the specified piece based on the number of pieces and empty slots in the window.
    The score is adjusted based on the presence of the opponent's pieces as well.

    Args:
        window (list): A list of four consecutive slots on the board.
        piece (int): The piece to evaluate the score for (e.g., BOT_PIECE or PLAYER_PIECE).

    Returns:
        int: The calculated score for the specified piece in the given window.
    """
        score = 0
        opp_piece = self.PLAYER_PIECE if piece == self.BOT_PIECE else self.BOT_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2
        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def get_ai_move(self, difficulty):
        """
    Get the AI's move based on the specified difficulty level.

    This method determines the best move for the AI based on the selected difficulty level.
    For "easy" difficulty, the AI makes random moves. For "medium" difficulty, the AI blocks
    human moves and checks for winning moves. For "hard" difficulty, the AI uses the Minimax
    algorithm with alpha-beta pruning to find the optimal move.

    Args:
        difficulty (str): The difficulty level of the AI ("easy", "medium", or "hard").

    Returns:
        int: The column index where the AI should place its piece, or None if no valid moves are available.
    """
        if difficulty == "easy":
            # Easy AI logic to make random moves
            valid_cols = [col for col in range(self.cols) if self.is_valid_move(col)]
            if valid_cols:
                return random.choice(valid_cols)
        elif difficulty == "medium":
            # Medium AI logic to block human moves and check for winning moves
            opponent = 3 - self.current_player
            for col in range(self.cols):
                if self.is_valid_move(col):
                    for row in reversed(range(self.rows)):
                        if self.board[row][col] == 0:
                            self.board[row][col] = self.current_player
                            if self.check_winner(row, col, self.current_player):
                                self.board[row][col] = 0
                                return col
                            self.board[row][col] = 0

                            self.board[row][col] = opponent
                            if self.check_winner(row, col, opponent):
                                self.board[row][col] = 0
                                return col
                            self.board[row][col] = 0
                            break
            valid_cols = [col for col in range(self.cols) if self.is_valid_move(col)]
            if valid_cols:
                return random.choice(valid_cols)
        elif difficulty == "hard":
            # Hard AI logic using minmax kinda
            column, _ = self.minimax(self.get_board_state(), depth=4, alpha=-9999999, beta=9999999, maximisingPlayer=True)
            return column
        return None

    