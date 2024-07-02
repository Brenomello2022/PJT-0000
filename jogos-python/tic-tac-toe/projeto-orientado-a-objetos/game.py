import pygame
import sys
import time
from settings import *

# Classe principal do jogo Tic-Tac-Toe
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")

        # Inicializar sons
        self.click_sound = pygame.mixer.Sound(CLICK_SOUND_FILE)
        self.button_sound = pygame.mixer.Sound(BUTTON_SOUND_FILE)

        # Inicializar o tabuleiro
        self.grid = [[None, None, None], [None, None, None], [None, None, None]]

        # Inicializar jogador
        self.player = "X"

        # Nome do jogador automático
        self.computer_name = "Computer"
        self.player_name = "Player"

        # Estado do jogo
        self.game_started = False
        self.game_over = False

        # Retângulos de interação
        self.new_game_rect = None
        self.start_button_rect = None
        self.end_game_rect = None
        self.play_again_button_rect = None

        # Relógio para controle de FPS
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        self.screen.fill(BLACK)
        for x in range(1, 3):
            pygame.draw.line(self.screen, self.interpolate_color(), (x * 200, 0), (x * 200, SCREEN_HEIGHT), 5)
        for y in range(1, 3):
            pygame.draw.line(self.screen, self.interpolate_color(), (0, y * 200), (SCREEN_WIDTH, y * 200), 5)

    def interpolate_color(self):
        color_index = int(time.time() * 2) % len(TRANSITION_COLORS)
        return TRANSITION_COLORS[color_index]

    def draw_moves(self):
        for y in range(3):
            for x in range(3):
                if self.grid[y][x] == "X":
                    self.draw_x(x, y)
                elif self.grid[y][x] == "O":
                    self.draw_o(x, y)

    def draw_x(self, x, y):
        pygame.draw.line(self.screen, PLAYER_COLORS["X"], (x * 200 + 30, y * 200 + 30), (x * 200 + 170, y * 200 + 170), 15)
        pygame.draw.line(self.screen, PLAYER_COLORS["X"], (x * 200 + 170, y * 200 + 30), (x * 200 + 30, y * 200 + 170), 15)

    def draw_o(self, x, y):
        pygame.draw.circle(self.screen, PLAYER_COLORS["O"], (x * 200 + 100, y * 200 + 100), 70, 15)

    def check_winner(self):
        for row in self.grid:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] and self.grid[0][col] is not None:
                return self.grid[0][col]
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] is not None:
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] is not None:
            return self.grid[0][2]
        return None

    def is_board_full(self):
        for row in self.grid:
            for cell in row:
                if cell is None:
                    return False
        return True

    def computer_move(self):
        for y in range(3):
            for x in range(3):
                if self.grid[y][x] is None:
                    self.grid[y][x] = "O"
                    return

    def draw_start_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 48)
        
        # Texto "New Game"
        text_new_game = font.render('New Game', True, WHITE)
        new_game_rect = text_new_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(text_new_game, new_game_rect)

        # Botão "Start"
        start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 100, 200, 50)
        pygame.draw.rect(self.screen, WHITE, start_button_rect, 3)  # Bordas brancas
        start_font = pygame.font.Font(None, 36)
        start_text = start_font.render('Start', True, WHITE)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)

        return new_game_rect, start_button_rect

    def draw_end_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 48)
        
        # Texto "Game Over"
        text_end_game = font.render('Game Over', True, WHITE)
        end_game_rect = text_end_game.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(text_end_game, end_game_rect)

        winner = self.check_winner()
        if winner == "X":
            winner_text = f"{self.player_name} wins!"
        elif winner == "O":
            winner_text = f"{self.computer_name} wins!"
        else:
            winner_text = "It's a draw!"

        # Texto do vencedor
        text_winner = font.render(winner_text, True, WHITE)
        winner_rect = text_winner.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 15))  # Ajuste na posição vertical
        self.screen.blit(text_winner, winner_rect)

        # Botão "Play Again"
        play_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 200, 200, 50)
        pygame.draw.rect(self.screen, WHITE, play_again_button_rect, 3)  # Bordas brancas
        play_again_font = pygame.font.Font(None, 36)
        play_again_text = play_again_font.render('Play Again', True, WHITE)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
        self.screen.blit(play_again_text, play_again_text_rect)

        return end_game_rect, play_again_button_rect

    def button_clicked(self, rect):
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            return True
        return False

    def reset_game(self):
        self.grid = [[None, None, None], [None, None, None], [None, None, None]]
        self.player = "X"
        self.end_game_rect = None  # Resetar para garantir que as telas sejam redesenhadas.
        self.play_again_button_rect = None
        self.button_sound.play()  # Reproduzir som de botão ao reiniciar o jogo.

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                    self.reset_game()
                    self.draw_grid()
                    pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.game_started:
                        if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                            self.game_started = True
                            self.reset_game()
                            self.draw_grid()
                            pygame.display.flip()
                    elif self.game_over:
                        if self.play_again_button_rect and self.play_again_button_rect.collidepoint(event.pos):
                            self.game_started = True
                            self.game_over = False
                            self.reset_game()
                            self.draw_grid()
                            pygame.display.flip()
                    elif self.player == "X":
                        x, y = event.pos
                        row = y // 200
                        col = x // 200
                        if self.grid[row][col] is None:
                            self.grid[row][col] = self.player
                            self.click_sound.play()
                            self.draw_grid()
                            self.draw_moves()
                            pygame.display.flip()
                            winner = self.check_winner()
                            if winner or self.is_board_full():
                                self.game_over = True
                                pygame.time.wait(1000)
                            else:
                                self.player = "O"
                                pygame.time.wait(1000)
                                self.computer_move()
                                self.draw_grid()
                                self.draw_moves()
                                pygame.display.flip()
                                winner = self.check_winner()
                                if winner or self.is_board_full():
                                    self.game_over = True
                                    pygame.time.wait(1000)
                                self.player = "X"

        if self.game_started and not self.game_over:
            self.draw_grid()
            self.draw_moves()
            pygame.display.flip()

        if self.game_over:
            if not self.end_game_rect or not self.play_again_button_rect:
                self.end_game_rect, self.play_again_button_rect = self.draw_end_screen()
                pygame.display.flip()

        if not self.game_started:
            if not self.new_game_rect or not self.start_button_rect:
                self.new_game_rect, self.start_button_rect = self.draw_start_screen()
                pygame.display.flip()

        self.clock.tick(30)
        return True

    def run_game(self):
        while self.handle_events():
            pass

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run_game()
