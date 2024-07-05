import pygame
import random
import time
from snake import Snake
from food import Food
from button import Button
from constants import *

# Classe com o loop principal.

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake_block = 10
        self.snake_speed = 15
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.button_sound = pygame.mixer.Sound("audios/button.wav")
        self.bite_sound = pygame.mixer.Sound("audios/bite.wav")
        self.game_over_sound = pygame.mixer.Sound("audios/game-over.wav")
        self.snake = Snake(self.screen, self.snake_block, self.bite_sound)
        self.food = Food(self.screen, self.snake_block)
        self.button_start = Button(self.screen, "Start", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)
        self.button_play_again = Button(self.screen, "Play Again", SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25, 150, 50)

    def start_screen(self):
        start = False
        while not start:
            self.screen.fill(BLACK)
            title = self.score_font.render("New Game", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            self.screen.blit(title, title_rect.topleft)

            if self.button_start.draw():
                self.button_sound.play()
                time.sleep(0.5)
                start = True

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def game_over_screen(self):
        self.game_over_sound.play()
        game_over = False
        while not game_over:
            self.screen.fill(BLACK)
            title = self.score_font.render("Game Over", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            self.screen.blit(title, title_rect.topleft)

            if self.button_play_again.draw():
                self.button_sound.play()
                time.sleep(0.5)
                self.gameLoop()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def gameLoop(self):
        game_over = False
        game_close = False

        # Reinicia a cobra e a comida.
        self.snake = Snake(self.screen, self.snake_block, self.bite_sound)
        self.food = Food(self.screen, self.snake_block)

        while not game_over:
            while game_close:
                self.game_over_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    self.snake.handle_keys(event.key)

            game_close = self.snake.move(self.food)

            self.screen.fill(BLACK)

            self.food.update_color()  
            self.food.draw()
            self.snake.draw()

            pygame.display.update()

            if self.snake.check_collision():
                game_close = True

            if self.snake.check_food_collision(self.food):
                self.food.move()

            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()