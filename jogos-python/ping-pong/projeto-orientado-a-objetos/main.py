# Imports.

import sys
import pygame
from pygame import mixer
from game import Game

# Inicializações.

pygame.init()
mixer.init()

# Configurações de tela.

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

# Inicializa o jogo.

game = Game(screen, width, height)
game.main_menu()

# Loop que controla a execução contínua do jogo, e também faz o jogo terminar.

while game.running:
    game.play()
    if not game.control:
        game.end_game()

pygame.quit()
sys.exit()