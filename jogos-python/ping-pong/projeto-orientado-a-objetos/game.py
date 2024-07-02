# Imports.

import sys
import pygame
import random
from pygame import mixer
from entities import Racket, Ball

# Definindo as configurações de fonte, largura, altura, controle etc.

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_file = "font/PressStart2P-Regular.ttf"
        self.font = pygame.font.Font(self.font_file, 20)
        self.clock = pygame.time.Clock()
        self.running = True
        self.control = False
        self.winner = ""

        self.racket_player1 = Racket(width - 20, height // 2 - 30, 10, 60, 5, height)
        self.racket_pc = Racket(10, height // 2 - 30, 10, 60, 5, height)
        self.ball = Ball(width // 2 - 5, height // 2 - 5, 10, 3, 3, width, height)

        self.score_player1 = 0
        self.score_pc = 0

        self.sound = mixer.Sound("audios/SoundA.wav")

    # Menu principal.

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.control = True
                        return

            self.screen.fill((0, 0, 0))
            text_menu = self.font.render("Ping Pong", True, (255, 255, 255))
            text_menu_rect = text_menu.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text_menu, text_menu_rect)

            time = pygame.time.get_ticks()
            if time % 2000 < 1000:
                text_start = self.font.render("Press Space", True, (255, 255, 255))
                text_start_rect = text_menu.get_rect(center=(380, 400))
                self.screen.blit(text_start, text_start_rect)

            pygame.display.flip()

    # Fim do jogo.

    def end_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.control = True
                        self.reset_game()
                        self.running = True
                        return

            self.screen.fill((0, 0, 0))
            text_end = self.font.render(f"Winner: {self.winner}", True, (255, 255, 255))
            text_end_rect = text_end.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text_end, text_end_rect)

            pygame.display.flip()

    # Reiniciando o jogo.

    def reset_game(self):
        self.racket_player1.reset(self.width - 20, self.height // 2 - 30)
        self.racket_pc.reset(10, self.height // 2 - 30)
        self.ball.reset(self.width // 2 - 5, self.height // 2 - 5)
        self.ball.reset_velocity()
        self.score_player1 = 0
        self.score_pc = 0

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill((0, 0, 0))
        self.ball.move()

        # Colisões e lógica de jogo.

        if self.ball.rect.colliderect(self.racket_pc.rect) or self.ball.rect.colliderect(self.racket_player1.rect):
            self.ball.bounce()
            self.sound.play()

        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.height:
            self.ball.bounce_vertical()

        if self.ball.rect.left <= 0:
            self.ball.reset(self.width // 2 - 5, self.height // 2 - 5)
            self.score_player1 += 1
            if self.score_player1 == 5:
                self.winner = "Player 1"
                self.control = False

        if self.ball.rect.right >= self.width:
            self.ball.reset(self.width // 2 - 5, self.height // 2 - 5)
            self.score_pc += 1
            if self.score_pc == 5:
                self.winner = "PC"
                self.control = False

        self.racket_pc.move_ai(self.ball.rect.centery)
        self.racket_pc.constrain()
        self.racket_player1.move(pygame.key.get_pressed())
        self.racket_player1.constrain()

        self.display_score()
        self.draw_elements()
        self.ball.increase_speed()

        pygame.display.flip()
        self.clock.tick(60)

    # Pontuação do PC e do Player.

    def display_score(self):
        font_score = pygame.font.Font(self.font_file, 16)
        score_text_pc = font_score.render(f"Score PC: {self.score_pc}", True, (255, 255, 255))
        score_rect_pc = score_text_pc.get_rect(center=(self.width // 4, 30))  # Centraliza no lado esquerdo

        score_text_player1 = font_score.render(f"Score Player1: {self.score_player1}", True, (255, 255, 255))
        score_rect_player1 = score_text_player1.get_rect(center=(3 * self.width // 4, 30))  # Centraliza no lado direito

        self.screen.blit(score_text_pc, score_rect_pc)
        self.screen.blit(score_text_player1, score_rect_player1)

    # Desenhando os elementos na tela.

    def draw_elements(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.racket_pc.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.racket_player1.rect)
        pygame.draw.ellipse(self.screen, self.ball.color, self.ball.rect)
        pygame.draw.aaline(self.screen, (255, 255, 255), (self.width // 2, 0), (self.width // 2, self.height))