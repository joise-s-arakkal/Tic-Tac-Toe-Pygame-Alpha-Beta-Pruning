import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 400  # Extra space for the message and retry button
LINE_COLOR = (255, 215, 0)
BG_COLOR = (25, 25, 25) 
FONT_COLOR = (255, 255, 255)
LINE_WIDTH = 5
CELL_SIZE = 100
BORDER_WIDTH = 5
BUTTON_COLOR = (34, 139, 34)
BUTTON_TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (10, 200, 0)

# Initialize screen and font
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
font = pygame.font.SysFont(None, 30)
button_font = pygame.font.SysFont(None, 30)

class TicTacToe:
    def __init__(self):
        self.current_player = "X"
        self.board = [[None]*3 for _ in range(3)]
        self.game_over = False
        self.message = ""
        self.winning_cells = []  # To store the winning cells
        self.retry_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 60, 120, 30)

    def draw_board(self):
        screen.fill(BG_COLOR)  # Fill the screen with the background color

        # Draw the cells first
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is not None:
                    # Determine the color based on whether the cell has a winning move
                    cell_color = HIGHLIGHT_COLOR if (row, col) in self.winning_cells else BG_COLOR
                    pygame.draw.rect(screen, cell_color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    
                    # Draw the marks (X and O) on the cell
                    if self.board[row][col] == "X":
                        self.draw_x(row, col)
                    elif self.board[row][col] == "O":
                        self.draw_o(row, col)

        # Draw the outer border
        pygame.draw.rect(screen, LINE_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 100), BORDER_WIDTH)

        # Draw the grid lines
        for row in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * row), (SCREEN_WIDTH, CELL_SIZE * row), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * row, 0), (CELL_SIZE * row, SCREEN_HEIGHT - 105), LINE_WIDTH)

        # Display message and retry button
        self.display_message(self.message)

    def draw_x(self, row, col, color=FONT_COLOR):
        start_pos = (col * CELL_SIZE + 20, row * CELL_SIZE + 20)
        end_pos = (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + CELL_SIZE - 20)
        pygame.draw.line(screen, color, start_pos, end_pos, LINE_WIDTH)
        start_pos = (col * CELL_SIZE + 20, row * CELL_SIZE + CELL_SIZE - 20)
        end_pos = (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + 20)
        pygame.draw.line(screen, color, start_pos, end_pos, LINE_WIDTH)

    def draw_o(self, row, col, color=FONT_COLOR):
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, color, center, CELL_SIZE // 2 - 20, LINE_WIDTH)

    def on_click(self, row, col):
        if self.board[row][col] is None and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.message = f"{self.current_player} Wins!" if self.current_player == "X" else "Computer Wins!"
                self.game_over = True
            elif self.check_draw():
                self.message = "It's a Draw!"
                self.game_over = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    row, col = self.computer_move()
                    self.on_click(row, col)

    def check_winner(self):
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                self.winning_cells = [(row, 0), (row, 1), (row, 2)]
                return True
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                self.winning_cells = [(0, col), (1, col), (2, col)]
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.winning_cells = [(0, 0), (1, 1), (2, 2)]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.winning_cells = [(0, 2), (1, 1), (2, 0)]
            return True
        return False

    def check_draw(self):
        for row in self.board:
            if None in row:
                return False
        return True

    def reset_game(self):
        self.board = [[None]*3 for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.message = ""
        self.winning_cells = []

    def display_message(self, message):
        # Display the message
        text_surface = font.render(message, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75))
        screen.blit(text_surface, text_rect)

        # Display retry button if the game is over
        if self.game_over:
            pygame.draw.rect(screen, BUTTON_COLOR, self.retry_button_rect)
            retry_text = button_font.render("Retry", True, BUTTON_TEXT_COLOR)
            retry_rect = retry_text.get_rect(center=self.retry_button_rect.center)
            screen.blit(retry_text, retry_rect)

    def check_retry_click(self, pos):
        if self.retry_button_rect.collidepoint(pos):
            self.reset_game()

    def computer_move(self):
        _, row, col = self.minimax(True)
        return row, col

    def evaluate(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2]:
                if self.board[row][0] == "X":
                    return -1
                elif self.board[row][0] == "O":
                    return 1
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col]:
                if self.board[0][col] == "X":
                    return -1
                elif self.board[0][col] == "O":
                    return 1
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == "X":
                return -1
            elif self.board[0][0] == "O":
                return 1
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == "X":
                return -1
            elif self.board[0][2] == "O":
                return 1
        return 0

    def minimax(self, is_player, alpha=-float('inf'), beta=float('inf')):
        utility_func_val = self.evaluate()
        if utility_func_val == 1 or utility_func_val == -1:
            return utility_func_val, None, None
        if self.check_draw():
            return 0, None, None

        if is_player:
            best = -float('inf')
            best_row, best_col = None, None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        self.board[i][j] = "O"
                        val, _, _ = self.minimax(False, alpha, beta)
                        self.board[i][j] = None
                        if val > best:
                            best = val
                            best_row, best_col = i, j
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best, best_row, best_col
        else:
            best = float('inf')
            best_row, best_col = None, None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        self.board[i][j] = "X"
                        val, _, _ = self.minimax(True, alpha, beta)
                        self.board[i][j] = None
                        if val < best:
                            best = val
                            best_row, best_col = i, j
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best, best_row, best_col

if __name__ == "__main__":
    game = TicTacToe()

    while True:
        game.draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < SCREEN_HEIGHT - 100:
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    game.on_click(row, col)
                elif game.game_over:
                    game.check_retry_click(event.pos)

        pygame.display.update()
