import pygame
import random

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da tela
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simon Says')

# Definir as cores
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
colors = [red, green, blue, yellow]

# Carregar os sons
button_sound = pygame.mixer.Sound('audios/button.wav')
correct_sound = pygame.mixer.Sound('audios/correct.wav')
wrong_sound = pygame.mixer.Sound('audios/wrong.wav')

# Inicializar o jogo
sequence = []
player_sequence = []
game_over = False
running = True
showing_sequence = False  # Variável para controlar a exibição da sequência

# Definir as fontes
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def start_screen():
    while running:
        screen.fill(black)
        draw_text('New Game', score_font, white, screen, screen_width // 2, screen_height // 2 - 50)
        start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2, 100, 50)
        
        # Verificar se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, green, start_button)
        else:
            pygame.draw.rect(screen, red, start_button)
        
        draw_text('Start', font_style, black, screen, screen_width // 2, screen_height // 2 + 25)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    button_sound.play()
                    return True

def game_over_screen():
    global game_over, sequence, player_sequence
    while game_over:
        screen.fill(black)
        draw_text('Game Over', score_font, white, screen, screen_width // 2, screen_height // 2 - 50)
        play_again_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2, 150, 50)
        
        # Verificar se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        if play_again_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, green, play_again_button)
        else:
            pygame.draw.rect(screen, red, play_again_button)
        
        draw_text('Play Again', font_style, black, screen, screen_width // 2, screen_height // 2 + 25)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    button_sound.play()
                    game_over = False
                    sequence = [random.randint(0, 3)]
                    player_sequence = []
                    show_sequence()
                    return True

# Função principal do jogo
def game_loop():
    global sequence, player_sequence, game_over, showing_sequence

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not showing_sequence:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(color_rects):
                    if rect.collidepoint(pos):
                        player_sequence.append(i)
                        print(f"Player clicked on color: {i}, Player sequence: {player_sequence}")

                        if player_sequence[-1] != sequence[len(player_sequence) - 1]:
                            wrong_sound.play()
                            game_over = True
                            print("Game Over: Player sequence does not match.")
                            if not game_over_screen():
                                return False
                        else:
                            print("Correct so far.")
                            if len(player_sequence) == len(sequence):
                                correct_sound.play()
                                player_sequence = []
                                sequence.append(random.randint(0, 3))
                                print(f"New sequence: {sequence}")
                                show_sequence()
                        break

        if game_over:
            if not game_over_screen():
                return False
        
        screen.fill(black)
        for i, rect in enumerate(color_rects):
            pygame.draw.rect(screen, colors[i], rect)

        # Desenhar as linhas de separação
        pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)
        pygame.draw.line(screen, white, (0, screen_height // 2), (screen_width, screen_height // 2), 5)

        pygame.display.flip()

    return True

def show_sequence():
    global showing_sequence
    showing_sequence = True  # Inicia a exibição da sequência
    for i in sequence:
        screen.fill(black)
        pygame.draw.rect(screen, colors[i], color_rects[i])
        pygame.display.flip()
        pygame.time.wait(800)  # Aumentar o tempo de exibição para 800ms
        screen.fill(black)
        pygame.display.flip()
        pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)
        pygame.draw.line(screen, white, (0, screen_height // 2), (screen_width, screen_height // 2), 5)
        pygame.time.wait(300)  # Esperar 300ms antes de exibir a próxima cor
    showing_sequence = False  # Termina a exibição da sequência

if __name__ == "__main__":
    color_rects = [
        pygame.Rect(0, 0, screen_width // 2, screen_height // 2),
        pygame.Rect(screen_width // 2, 0, screen_width // 2, screen_height // 2),
        pygame.Rect(0, screen_height // 2, screen_width // 2, screen_height // 2),
        pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 2)
    ]
    sequence.append(random.randint(0, 3))
    print(f"Initial sequence: {sequence}")
    
    if start_screen():
        show_sequence()
        while running:
            if not game_loop():
                break
    
    pygame.quit()
    print("Player has quit the game.")
