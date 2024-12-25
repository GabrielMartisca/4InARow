import pygame
import sys
from connect4 import Connect4

pygame.init()

WIDTH, HEIGHT = 700, 600
#SQUARESIZE = 100
#RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")
pygame.font.init()
font = pygame.font.SysFont("monospace", 75)

def display_message(message):
    label = font.render(message, 1, WHITE)
    screen.blit(label, (40, 10))
    pygame.display.update()

def draw_board(game):
    for row in range(game.rows):
        SQUARESIZE = min(WIDTH // game.cols, HEIGHT // (game.rows))
        RADIUS = int(SQUARESIZE / 2 - 5)
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
    

def check_draw(game):
    for col in range(game.cols):
        if game.is_valid_move(col):
            return False
    return True

def main():
    game = Connect4(rows=6, cols=7, p1="human", p2="human")
    game_over = False
    human_turn = game.players[game.current_player] == "human"

    SQUARESIZE = min(WIDTH // game.cols, HEIGHT // (game.rows ))
    RADIUS = int(SQUARESIZE / 2 - 5)
    draw_board(game)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if human_turn:
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

                    move = game.make_move(col)
                    if move:  
                        row, col = move
                        if game.check_winner(row, col):
                            draw_board(game)
                            display_message(f"Player {game.current_player} wins!")
                            game_over = True
                        elif check_draw(game):
                            draw_board(game)
                            display_message("Draw!")
                        else:
                            game.switch_player()
                            human_turn = game.players[game.current_player] == "human"
                        draw_board(game)
                    else:
                        print(f"Column {col} is full. Try again!")
            else:
                # AI's turn
                col = game.get_ai_move(difficulty=game.players[game.current_player])
                if col is not None:
                    move = game.make_move(col)
                    if move:  
                        row, col = move
                        if game.check_winner(row, col):
                            draw_board(game)
                            display_message(f"Player {game.current_player} wins!")
                            game_over = True
                        elif check_draw(game):
                            draw_board(game)
                            display_message("Draw!")
                        else:
                            game.switch_player()
                            human_turn = game.players[game.current_player] == "human"
                        draw_board(game)
                else:
                    print("No valid moves available for AI. Game over.")
                    game_over = True

        if game_over:
            pygame.time.wait(7000)  

if __name__ == "__main__":
    main()