import random

class Connect4:
    def __init__(self, rows=6, cols=7, p1="human", p2="human"):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_player = 1
        self.players = {1: p1, 2: p2}

    def make_move(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return row, col
        return None

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def check_winner(self, row, col):
        def count_consecutive_tokens(dr, dc):
            count = 0
            r, c = row, col
            while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == self.current_player:
                count += 1
                r += dr
                c += dc
            return count - 1

        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            if count_consecutive_tokens(dr, dc) + count_consecutive_tokens(-dr, -dc) >= 3:
                return True
        return False

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

    def get_ai_move(self, difficulty):
        if difficulty == "easy":
            # Easy AI logic to make random moves
            valid_cols = [col for col in range(self.cols) if self.is_valid_move(col)]
            if valid_cols:
                return random.choice(valid_cols)
        elif difficulty == "medium":
            # Medium AI logic to block human moves
            opponent = 3 - self.current_player
            for col in range(self.cols):
                if self.is_valid_move(col):
                    for row in reversed(range(self.rows)):
                        if self.board[row][col] == 0:
                            self.board[row][col] = opponent
                            if self.check_winner(row, col):
                                self.board[row][col] = 0  
                                return col  
                            self.board[row][col] = 0  
                            break  


        valid_cols = [col for col in range(self.cols) if self.is_valid_move(col)]
        if valid_cols:
            return random.choice(valid_cols)
        elif difficulty == "hard":
            # Hard AI logic (to be implemented)
            pass
        return None