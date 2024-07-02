# Imports.

import pygame
import sys

# Configurações iniciais, variáveis e definições.

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

# Definição das propriedades da raquete.

racket_width = 10
racket_height = 60
ball_size = 10

# Velocidade da raquete.

racket_player1_dy = 5  # dy significa velocidade
racket_pc_dy = 5

# Velocidade da bola.

velocity_bx = 3
velocity_by = 3

# Definir vencedor.

winner = ""

# Definir Controle.

running = True
control = False

# Configuração da fonte.

font_file = "font/PressStart2P-Regular.ttf"
font = pygame.font.Font(font_file, 20)

# Taxa de quadros.

clock = pygame.time.Clock()

# Criando o Menu do Jogo

def main_menu():
    global running, control
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    control = True
                    return

        # Renderiza o texto do menu.
                    
        screen.fill(BLACK)
        text_menu = font.render("Ping Pong", True, WHITE)
        text_menu_rect = text_menu.get_rect(center=(width // 2, height // 2))   
        screen.blit(text_menu, text_menu_rect)

        time = pygame.time.get_ticks()

        # Pressione espaço para jogar.

        if time % 2000 < 1000:
            text_start = font.render("Press Space", True, WHITE)
            text_start_rect = text_menu.get_rect(center=(380, 400))
            screen.blit(text_start, text_start_rect)

        pygame.display.flip()

# Posição Inicioal das variaveis.

def starting_position():
    global pc_x, pc_y, player1_x, player1_y, ball_x, ball_y, score_pc, score_player1

    # Posição da raquete do PC.

    pc_x = 10
    pc_y = height // 2 - racket_height // 2

    # Pocição da raquete do Player.

    player1_x = width - 20  # Aqui é 20 pois o tamanho da raquete ja é 10, então adicionamos + 10, por isso diminuimos 20, e não 10.
    player1_y = height // 2 - racket_height // 2

    # Posição da bola.

    ball_x = width // 2 - ball_size // 2
    ball_y = height // 2 - ball_size // 2

    # Define o Score (Pontuação).

    score_player1 = 0
    score_pc = 0
    
# Fim do jogo

def end_game():
    global running, winner, control
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    control = True
                    starting_position()
                    running = True
                    return
                
        # Renderiza o Texto do Menu.

        screen.fill(BLACK)
        text_end = font.render(f"Winner: {winner}", True, WHITE)
        text_end_rect = text_end.get_rect(center=(width // 2, height // 2))
        screen.blit(text_end, text_end_rect)

        pygame.display.flip()    
    
main_menu()
starting_position()

# Mecânica do Loop Infinito.

while running:
    if not control:
        end_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Movendo a bola.

        ball_x += velocity_bx
        ball_y += velocity_by

        # Retângulos de colisão.

        ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)
        racket_pc_rect = pygame.Rect(pc_x, pc_y, racket_width, racket_height)
        racket_player1_rect = pygame.Rect(player1_x, player1_y, racket_width, racket_height)
        
        # Colisão da bola com a raquete do pc e a raquete do player.

        if ball_rect.colliderect(racket_pc_rect) or ball_rect.colliderect(racket_player1_rect):
            velocity_bx = - velocity_bx

        # Colisão da bola com as bordas da tela.
        
        if ball_y <= 0 or ball_y >= height - ball_size:
            velocity_by = - velocity_by
        
        # Posicionar a bola no inicio do jogo.
            
        if ball_x <= 0:
            ball_x = width // 2 - ball_size // 2
            ball_y = height // 2 - ball_size // 2
            velocity_bx = - velocity_bx
            score_player1 += 1
            print(f"Score Player1: {score_player1}")
            if score_player1 == 5:
                print("Player_1 won!")
                winner = "Player 1"
                end_game()
        
        if ball_x >= width - ball_size:
            ball_x = width // 2 - ball_size // 2
            ball_y = height // 2 - ball_size // 2
            velocity_bx = - velocity_bx
            score_pc += 1
            print(f"Score PC: {score_pc}")
            if score_pc == 5:
                print("PC won!")
                winner = "PC"
                end_game()

        # Movendo a raquete do PC para seguir a bola.
            
        if pc_y + racket_height // 2 < ball_y:
            pc_y += racket_pc_dy
        elif pc_y + racket_height // 2 > ball_y:
            pc_y -= racket_pc_dy
        
        # Evitar que a raquete do PC saia da área.
        
        if pc_y < 0:
            pc_y = 0
        elif pc_y > height - racket_height:
            pc_y = height - racket_height

        # Mostrando o Score do Jogo.

        fonte_score = pygame.font.Font(font_file, 16)        
        score_text = font.render(
            f"Score PC: {score_pc}        Score Player1: {score_player1}", True, WHITE
        )
        score_rect = score_text.get_rect(center=(width // 2, 30))

        screen.blit(score_text, score_rect)

        # Desenhando os elementos na tela.

        pygame.draw.rect(screen, WHITE, (pc_x, pc_y, racket_width, racket_height))                   # Desenhando a raquete esquerda.
        pygame.draw.rect(screen, WHITE, (player1_x, player1_y, racket_width, racket_height))         # Desenhando a raquete direita.
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))                   # Desenhando a bola.
        pygame.draw.aaline(screen, WHITE, (width // 2, 0), (width // 2, height))                     # Desenhando a linha do meio

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and player1_y > 0:
            player1_y -= racket_player1_dy
        if keys[pygame.K_DOWN] and player1_y < height - racket_height:
            player1_y += racket_player1_dy

        pygame.display.flip()

        clock.tick(60)

pygame.quit()
sys.exit()
