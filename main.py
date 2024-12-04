import pygame
import sys
from connect4 import Connect4

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 600
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# Draw the board
def draw_board(game):
    for row in range(game.rows):
        for col in range(game.cols):
            pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE + SQUARESIZE/2), int(row*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    
    for row in range(game.rows):
        for col in range(game.cols):
            if game.board[row][col] == 1:
                pygame.draw.circle(screen, RED, (int(col*SQUARESIZE + SQUARESIZE/2), int((row - 1) * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif game.board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (int(col*SQUARESIZE + SQUARESIZE/2), int((row - 1) * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()
    

# Main game loop
def main():
    game = Connect4()
    game_over = False

    draw_board(game)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if game.current_player == 1:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                col = posx // SQUARESIZE

                # Attempt to make a move in the selected column
                move = game.make_move(col)
                if move:  # If the move is valid
                    row, col = move
                    if game.check_winner(row, col):
                        print(f"Player {game.current_player} wins!")
                        game_over = True
                    else:
                        game.switch_player()
                    draw_board(game)
                else:
                    print(f"Column {col} is full. Try again!")

if __name__ == "__main__":
    main()
