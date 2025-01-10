import pygame
import sys
from connect4 import Connect4

pygame.init()

WIDTH, HEIGHT = 700, 700
#SQUARESIZE = 100
#RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4 in a ROW")
pygame.font.init()
font = pygame.font.SysFont("monospace", 75)
small_font=pygame.font.SysFont("monospace", 40)
smaller_font=pygame.font.SysFont("monospace", 20)

def display_message(message):
    """
    Display a message on the screen.

    This method renders the specified message and displays it at a fixed position
    on the screen.

    Args:
        message (str): The message to display on the screen.

    Returns:
        None
    """
    label = font.render(message, 1, WHITE)
    screen.blit(label, (40, 10))
    pygame.display.update()

def draw_board(game):
    """
    Draw the game board on the screen.

    This method draws the Connect 4 game board on the screen, including the grid and the pieces.
    It first draws the grid with blue rectangles and black circles, and then it draws the pieces
    (red and yellow circles) based on the current state of the game board.

    Args:
        game (Connect4): The Connect 4 game instance containing the board state and dimensions.

    Returns:
        None
    """
    for row in range(game.rows):
        SQUARESIZE = min(WIDTH // game.cols, HEIGHT // (game.rows + 1)) 
        RADIUS = int(SQUARESIZE / 2 - 5)
        for col in range(game.cols):
            pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, (row+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE)) 
            pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE + SQUARESIZE/2), int((row+1) * SQUARESIZE + SQUARESIZE/2)), RADIUS)

    for row in range(game.rows):
        for col in range(game.cols):
            if game.board[row][col] == 1:
                pygame.draw.circle(screen, RED, (int(col*SQUARESIZE + SQUARESIZE/2), int(row * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif game.board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (int(col*SQUARESIZE + SQUARESIZE/2), int(row * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

    pygame.display.update()

def check_draw(game):
    """
    Check if the game is a draw.

    This method checks if the game board is full and no more valid moves can be made,
    indicating that the game has ended in a draw.

    Args:
        game (Connect4): The Connect 4 game instance containing the board state and dimensions.

    Returns:
        bool: True if the game is a draw (no valid moves left), False otherwise.
    """
    for col in range(game.cols):
        if game.is_valid_move(col):
            return False
    return True

def draw_text(text, font, color, surface, x, y):
    """
    Draw text on the screen.

    This method renders the specified text using the given font and color,
    and blits it onto the specified surface at the given coordinates.

    Args:
        text (str): The text to be rendered and displayed.
        font (pygame.font.Font): The font to use for rendering the text.
        color (tuple): The color of the text (e.g., (255, 255, 255) for white).
        surface (pygame.Surface): The surface to blit the rendered text onto.
        x (int): The x-coordinate of the top-left corner of the text.
        y (int): The y-coordinate of the top-left corner of the text.

    Returns:
        None
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    """
    Display the main menu and handle user interactions.

    This method displays the main menu with options to play the game, view how to play instructions,
    or exit the application. It handles user interactions with the menu buttons.

    Returns:
        None
    """
    click=False
    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_play = pygame.Rect(50, 100, 200, 50)
        button_how_to_play = pygame.Rect(50, 200, 350, 50)
        button_exit = pygame.Rect(50, 300, 200, 50)

        if button_play.collidepoint((mx, my)):
            if click:
                play_menu()
        if button_how_to_play.collidepoint((mx, my)):
            if click:
                how_to_play()
        if button_exit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, GREEN, button_play)
        pygame.draw.rect(screen, GREEN, button_how_to_play)
        pygame.draw.rect(screen, GREEN, button_exit)

        draw_text('Play', small_font, BLACK, screen, 60, 110)
        draw_text('How to Play', small_font, BLACK, screen, 60, 210)
        draw_text('Exit', small_font, BLACK, screen, 60, 310)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def draw_small_text(text, font, color, surface, x, y, max_width):
    """
    Draw text on the screen with word wrapping.

    This method renders the specified text using the given font and color,
    and blits it onto the specified surface at the given coordinates. The text
    is wrapped to fit within the specified maximum width.

    Args:
        text (str): The text to be rendered and displayed.
        font (pygame.font.Font): The font to use for rendering the text.
        color (tuple): The color of the text (e.g., (255, 255, 255) for white).
        surface (pygame.Surface): The surface to blit the rendered text onto.
        x (int): The x-coordinate of the top-left corner of the text.
        y (int): The y-coordinate of the top-left corner of the text.
        max_width (int): The maximum width of the text before wrapping to a new line.

    Returns:
        None
    """
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()
        if current_width + word_width >= max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width + font.size(' ')[0]  # Add space width
        else:
            current_line.append(word)
            current_width += word_width + font.size(' ')[0]  # Add space width

    lines.append(' '.join(current_line))  # Add the last line

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * word_height))


def how_to_play():
    """
    Display the 'How to Play' screen and handle user interactions.

    This method displays the instructions for playing the game and provides a 'Back' button
    to return to the main menu. It handles user interactions with the 'Back' button.

    Returns:
        None
    """
    while True:
        screen.fill(BLACK)
        draw_text('How to Play 4 in a ROW:', small_font, WHITE, screen, 20, 20)
        draw_small_text('The objective of 4 in a ROW is to be the first player to connect four of your pieces in a row, either horizontally, vertically, or diagonally. The game is played on a vertical grid with 7 columns and 6 rows, and each player is assigned a color (e.g., red or yellow). Players take turns dropping one piece into any column, where it will fall to the lowest available slot. To win, align four of your pieces in a straight line before your opponent does. If the grid fills completely without any player connecting four, the game ends in a draw. Plan your moves strategically to block your opponent while setting up your own winning pattern, and watch for diagonal opportunities—they can be easy to miss! Good luck and have fun!', smaller_font, WHITE, screen, 20, 100, WIDTH - 40)

        mx, my = pygame.mouse.get_pos()

        button_back = pygame.Rect(50, 500, 200, 50)
        if button_back.collidepoint((mx, my)):
            if click:
                main_menu()

        pygame.draw.rect(screen, GREEN, button_back)
        draw_text('Back', small_font, BLACK, screen, 60, 510)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def play_menu():
    """
    Display the play menu and handle user interactions.

    This method displays the play menu with options to play Player vs Player (PvP) or Player vs Computer (PvC).
    It also provides a 'Back' button to return to the main menu. It handles user interactions with the menu buttons.

    Returns:
        None
    """
    click=False
    while True:
        screen.fill(BLACK)
        draw_text('Play Menu', small_font, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_pvp = pygame.Rect(50, 100, 450, 50)
        button_pvc = pygame.Rect(50, 200, 450, 50)
        button_back = pygame.Rect(50, 300, 200, 50)

        if button_pvp.collidepoint((mx, my)):
            if click:
                choose_table_size("pvp", "human")
        if button_pvc.collidepoint((mx, my)):
            if click:
                difficulty_menu()
        if button_back.collidepoint((mx, my)):
            if click:
                main_menu()

        pygame.draw.rect(screen, GREEN, button_pvp)
        pygame.draw.rect(screen, GREEN, button_pvc)
        pygame.draw.rect(screen, GREEN, button_back)

        draw_text('Player vs Player', small_font, BLACK, screen, 60, 110)
        draw_text('Player vs Computer', small_font, BLACK, screen, 60, 210)
        draw_text('Back', small_font, BLACK, screen, 60, 310)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def choose_table_size(difficulty, first_player):
    """
    Display the table size selection menu and handle user interactions.

    This method displays the table size selection menu with options to choose different table sizes.
    It also provides a 'Back' button to return to the previous menu. It handles user interactions
    with the menu buttons.

    Args:
        difficulty (str): The difficulty level of the game.
        first_player (str): The player who goes first ("human" or "ai").

    Returns:
        None
    """
    click = False
    while True:
        screen.fill(BLACK)
        draw_text('Choose Table Size', small_font, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_6x7 = pygame.Rect(50, 100, 300, 50)
        button_8x8 = pygame.Rect(50, 200, 300, 50)
        button_10x10 = pygame.Rect(50, 300, 300, 50)
        button_back = pygame.Rect(50, 400, 200, 50)

        if button_6x7.collidepoint((mx, my)):
            if click:
                start_game(difficulty, first_player, 6, 7)
        if button_8x8.collidepoint((mx, my)):
            if click:
                start_game(difficulty, first_player, 8, 8)
        if button_10x10.collidepoint((mx, my)):
            if click:
                start_game(difficulty, first_player, 10, 10)
        if button_back.collidepoint((mx, my)):
            if click:
                if difficulty == "pvp":
                    play_menu()
                else:
                    choose_first_player(difficulty)

        pygame.draw.rect(screen, GREEN, button_6x7)
        pygame.draw.rect(screen, GREEN, button_8x8)
        pygame.draw.rect(screen, GREEN, button_10x10)
        pygame.draw.rect(screen, GREEN, button_back)

        draw_text('6x7', small_font, BLACK, screen, 60, 110)
        draw_text('8x8', small_font, BLACK, screen, 60, 210)
        draw_text('10x10', small_font, BLACK, screen, 60, 310)
        draw_text('Back', small_font, BLACK, screen, 60, 410)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def choose_first_player(difficulty):
    """
    Display the first player selection menu and handle user interactions.

    This method displays the first player selection menu with options to choose whether the human
    or the AI goes first. It also provides a 'Back' button to return to the previous menu.
    It handles user interactions with the menu buttons.

    Args:
        difficulty (str): The difficulty level of the game.

    Returns:
        None
    """
    click = False
    while True:
        screen.fill(BLACK)
        draw_text('Who Goes First?', small_font, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_human_first = pygame.Rect(50, 100, 300, 50)
        button_ai_first = pygame.Rect(50, 200, 300, 50)
        button_back = pygame.Rect(50, 300, 200, 50)

        if button_human_first.collidepoint((mx, my)):
            if click:
                choose_table_size(difficulty, "human")
        if button_ai_first.collidepoint((mx, my)):
            if click:
                choose_table_size(difficulty, "ai")
        if button_back.collidepoint((mx, my)):
            if click:
                difficulty_menu()

        pygame.draw.rect(screen, GREEN, button_human_first)
        pygame.draw.rect(screen, GREEN, button_ai_first)
        pygame.draw.rect(screen, GREEN, button_back)

        draw_text('Human First', small_font, BLACK, screen, 60, 110)
        draw_text('AI First', small_font, BLACK, screen, 60, 210)
        draw_text('Back', small_font, BLACK, screen, 60, 310)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def difficulty_menu():
    """
    Display the difficulty selection menu and handle user interactions.

    This method displays the difficulty selection menu with options to choose the game difficulty level.
    It also provides a 'Back' button to return to the previous menu. It handles user interactions
    with the menu buttons.

    Returns:
        None
    """
    click=False
    while True:
        screen.fill(BLACK)
        draw_text('Select Difficulty', small_font, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_easy = pygame.Rect(50, 100, 200, 50)
        button_medium = pygame.Rect(50, 200, 200, 50)
        button_hard = pygame.Rect(50, 300, 200, 50)
        button_back = pygame.Rect(50, 400, 200, 50)

        if button_easy.collidepoint((mx, my)):
            if click:
                choose_first_player("easy")
        if button_medium.collidepoint((mx, my)):
            if click:
                choose_first_player("medium")
        if button_hard.collidepoint((mx, my)):
            if click:
                choose_first_player("hard")
        if button_back.collidepoint((mx, my)):
            if click:
                play_menu()

        pygame.draw.rect(screen, GREEN, button_easy)
        pygame.draw.rect(screen, GREEN, button_medium)
        pygame.draw.rect(screen, GREEN, button_hard)
        pygame.draw.rect(screen, GREEN, button_back)

        draw_text('Easy', small_font, BLACK, screen, 60, 110)
        draw_text('Medium', small_font, BLACK, screen, 60, 210)
        draw_text('Hard', small_font, BLACK, screen, 60, 310)
        draw_text('Back', small_font, BLACK, screen, 60, 410)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def start_game(difficulty, first_player, rows=6, cols=7):
    """
    Start the game with the specified difficulty, first player, and table size.

    This method initializes the game with the given difficulty, first player, and table size.
    It handles the game loop, including player and AI moves, checking for a winner, and handling a draw.

    Args:
        difficulty (str): The difficulty level of the game ("pvp", "easy", "medium", "hard").
        first_player (str): The player who goes first ("human" or "ai").
        rows (int, optional): The number of rows in the game board. Defaults to 6.
        cols (int, optional): The number of columns in the game board. Defaults to 7.

    Returns:
        None
    """
    if difficulty == "pvp":
        game = Connect4(rows=rows, cols=cols, p1="human", p2="human")
    else:
        game = Connect4(rows=rows, cols=cols, p1="human", p2=difficulty)
    
    if first_player == "ai":
        game.current_player = 2  # AI goes first
    else:
        game.current_player = 1  # Human goes first
    game_over = False
    human_turn = game.players[game.current_player] == "human"

    SQUARESIZE = min(WIDTH // game.cols, HEIGHT // (game.rows))
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
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    col = posx // SQUARESIZE

                    move = game.make_move(col)
                    if move:
                        row, col = move
                        if game.check_winner(row, col, game.current_player):
                            draw_board(game)
                            display_message(f"Player {game.current_player} wins!")
                            game_over = True
                        elif check_draw(game):
                            draw_board(game)
                            display_message("Draw!")
                            game_over = True
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
                        if game.check_winner(row, col, game.current_player):
                            draw_board(game)
                            display_message(f"Player {game.current_player} wins!")
                            game_over = True
                        elif check_draw(game):
                            draw_board(game)
                            display_message("Draw!")
                            game_over = True
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
    """
    Main entry point of the application.

    This block of code runs when the script is executed directly. It starts the application
    by displaying the main menu.
    """
    main_menu()