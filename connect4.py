import random

class Connect4:
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
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return row, col
        return None

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def is_terminal_node(self, board):
        return self.winning_move(board, self.BOT_PIECE) or self.winning_move(board, self.PLAYER_PIECE) or self.check_draw()

    def winning_move(self, board, piece):
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
        for r in range(self.ROW_COUNT - 1, -1, -1):
            if board[r][col] == 0:  
                return r
        return None  

    def print_board(self):
        for row in self.board:
            print(" | ".join(str(cell) for cell in row))
        print("-" * (self.cols * 4 - 1))
        print()

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def check_winner(self, row, col, player):
        def count_consecutive_tokens(dr, dc):
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
        for col in range(self.cols):
            if self.is_valid_move(col):
                return False
        return True

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def reset_game(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1

    def print_board(self):
        for row in self.board:
            print(" | ".join(str(cell) for cell in row))
        print("-" * (self.cols * 4 - 1))
        print()

    def get_board_state(self):
        return self.board

    def get_valid_locations(self, board):
        return [col for col in range(self.COLUMN_COUNT) if self.is_valid_move(col)]

    def minimax(self, board, depth, alpha, beta, maximisingPlayer):
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

    