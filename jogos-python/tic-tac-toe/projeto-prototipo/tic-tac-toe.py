import pygame
import sys
import time

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da tela
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac Toe")

# Definir as cores das telas.
black = (0, 0, 0)
white = (255, 255, 255)

# Definir as cores das linhas do tabuleiro.
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
cyan = (0, 255, 255)
orange = (255, 165, 0)
pink = (255, 192, 203)
brown = (165, 42, 42)
dark_green = (0, 100, 0)
light_blue = (173, 216, 230)
gray = (128, 128, 128)
light_gray = (211, 211, 211)
magenta = (255, 0, 255)

# Cores para os jogadores
player_colors = {
    "X": red,
    "O": blue
}

# Cores para transição suave.
transition_colors = [red, green, blue, yellow, purple, cyan, orange, pink, brown, dark_green, light_blue, gray, light_gray, magenta]

# Carregar os sons.
click_sound = pygame.mixer.Sound("audios/click_sound.wav")
button_sound = pygame.mixer.Sound("audios/button.wav")

# Inicializar o tabuleiro.
grid = [[None, None, None], [None, None, None], [None, None, None]]

# Inicializar o jogador.
player = "X"

# Nome do jogador automático.
computer_name = "Computer"
player_name = "Player"

# Função para desenhar o tabuleiro com linhas de cores alternadas.
def draw_grid():
    screen.fill(black)
    for x in range(1, 3):
        pygame.draw.line(screen, interpolate_color(), (x * 200, 0), (x * 200, 600), 5)
    for y in range(1, 3):
        pygame.draw.line(screen, interpolate_color(), (0, y * 200), (600, y * 200), 5)

def interpolate_color():
    color_index = int(time.time() * 2) % len(transition_colors)  # Ajustar velocidade da transição.
    return transition_colors[color_index]

# Função para desenhar os movimentos.
def draw_moves():
    for y in range(3):
        for x in range(3):
            if grid[y][x] == "X":
                draw_x(x, y)
            elif grid[y][x] == "O":
                draw_o(x, y)

def draw_x(x, y):
    pygame.draw.line(screen, player_colors["X"], (x * 200 + 30, y * 200 + 30), (x * 200 + 170, y * 200 + 170), 15)
    pygame.draw.line(screen, player_colors["X"], (x * 200 + 170, y * 200 + 30), (x * 200 + 30, y * 200 + 170), 15)

def draw_o(x, y):
    pygame.draw.circle(screen, player_colors["O"], (x * 200 + 100, y * 200 + 100), 70, 15)

# Função para verificar se há um vencedor.
def check_winner():
    for row in grid:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] and grid[0][col] is not None:
            return grid[0][col]
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] is not None:
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] is not None:
        return grid[0][2]
    return None

# Função para verificar se o tabuleiro está cheio.
def is_board_full():
    for row in grid:
        for cell in row:
            if cell is None:
                return False
    return True

# Função para o movimento do jogador automático.
def computer_move():
    for y in range(3):
        for x in range(3):
            if grid[y][x] is None:
                grid[y][x] = "O"
                return

# Função para desenhar a tela de início.
def draw_start_screen():
    screen.fill(black)
    font = pygame.font.Font(None, 48)
    
    # Texto "New Game".
    text_new_game = font.render('New Game', True, white)
    new_game_rect = text_new_game.get_rect(center=(screen_width // 2, screen_height // 3))
    screen.blit(text_new_game, new_game_rect)

    # Botão "Start".
    start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 3 + 100, 200, 50)
    pygame.draw.rect(screen, white, start_button_rect, 3)  # Bordas brancas
    start_font = pygame.font.Font(None, 36)
    start_text = start_font.render('Start', True, white)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    return new_game_rect, start_button_rect

# Função para desenhar a tela de fim de jogo.
def draw_end_screen():
    screen.fill(black)
    font = pygame.font.Font(None, 48)
    
    # Texto "Game Over".
    text_end_game = font.render('Game Over', True, white)
    end_game_rect = text_end_game.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(text_end_game, end_game_rect)

    winner = check_winner()
    if winner == "X":
        winner_text = f"{player_name} wins!"
    elif winner == "O":
        winner_text = f"{computer_name} wins!"
    else:
        winner_text = "It's a draw!"

    # Texto do vencedor.
    text_winner = font.render(winner_text, True, white)
    winner_rect = text_winner.get_rect(center=(screen_width // 2, screen_height // 2 - 15))  # Ajuste na posição vertical
    screen.blit(text_winner, winner_rect)

    # Botão "Play Again".
    play_again_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 3 + 200, 200, 50)
    pygame.draw.rect(screen, white, play_again_button_rect, 3)  # Bordas brancas
    play_again_font = pygame.font.Font(None, 36)
    play_again_text = play_again_font.render('Play Again', True, white)
    play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
    screen.blit(play_again_text, play_again_text_rect)

    return end_game_rect, play_again_button_rect

# Função para verificar se o botão foi clicado.
def button_clicked(rect):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        return True
    return False

# Função para limpar o tabuleiro e reiniciar o jogo.
def reset_game():
    global grid, player, end_game_rect, play_again_button_rect
    grid = [[None, None, None], [None, None, None], [None, None, None]]
    player = "X"
    end_game_rect = None  # Resetar para garantir que as telas sejam redesenhadas.
    play_again_button_rect = None
    button_sound.play()  # Reproduzir som de botão ao reiniciar o jogo.

# Estado inicial do jogo.
game_started = False
game_over = False
new_game_rect = None
start_button_rect = None
end_game_rect = None
play_again_button_rect = None

# Loop principal do jogo.
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True
                reset_game()
                draw_grid()
                pygame.display.flip()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not game_started:
                    if start_button_rect and start_button_rect.collidepoint(event.pos):
                        game_started = True
                        reset_game()
                        draw_grid()
                        pygame.display.flip()
                elif game_over:
                    if play_again_button_rect and play_again_button_rect.collidepoint(event.pos):
                        game_started = True
                        game_over = False
                        reset_game()
                        draw_grid()
                        pygame.display.flip()
                elif player == "X":  # Garantir que apenas o jogador "X" pode jogar.
                    x, y = event.pos
                    row = y // 200
                    col = x // 200
                    if grid[row][col] is None:
                        grid[row][col] = player
                        click_sound.play()  # Reproduzir som de clique ao fazer uma jogada.
                        draw_grid()
                        draw_moves()
                        pygame.display.flip()
                        winner = check_winner()
                        if winner or is_board_full():
                            game_over = True
                            pygame.time.wait(1000)  # Espera antes de mostrar a tela de fim de jogo.
                        else:
                            player = "O"
                            time.sleep(1)  # Pausa antes do movimento do PC.
                            computer_move()
                            draw_grid()
                            draw_moves()
                            pygame.display.flip()
                            winner = check_winner()
                            if winner or is_board_full():
                                game_over = True
                                pygame.time.wait(1000)  # Espera antes de mostrar a tela de fim de jogo.
                            player = "X"  # Restaurar para o próximo turno do jogador "X".

    if game_started and not game_over:
        draw_grid()
        draw_moves()
        pygame.display.flip()

    if game_over:
        if not end_game_rect or not play_again_button_rect:
            end_game_rect, play_again_button_rect = draw_end_screen()
            pygame.display.flip()

    if not game_started:
        if not new_game_rect or not start_button_rect:
            new_game_rect, start_button_rect = draw_start_screen()
            pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()
