import pygame
import random
from constants import *

class Snake:
    def __init__(self, screen, block_size, bite_sound):
        self.screen = screen
        self.block_size = block_size
        self.snake_list = [[SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]]
        self.snake_speed = 10
        self.snake_direction = None 
        self.font_style = pygame.font.SysFont(None, 50)
        self.bite_sound = bite_sound
        self.moving = False

    def handle_keys(self, key):
        if key == pygame.K_LEFT and self.snake_direction != "RIGHT":
            self.snake_direction = "LEFT"
            self.moving = True
        elif key == pygame.K_RIGHT and self.snake_direction != "LEFT":
            self.snake_direction = "RIGHT"
            self.moving = True
        elif key == pygame.K_UP and self.snake_direction != "DOWN":
            self.snake_direction = "UP"
            self.moving = True
        elif key == pygame.K_DOWN and self.snake_direction != "UP":
            self.snake_direction = "DOWN"
            self.moving = True

    def move(self, food):
        if not self.moving:
            return False

        if self.snake_direction == "UP":
            new_head = [self.snake_list[0][0], self.snake_list[0][1] - self.block_size]
        elif self.snake_direction == "DOWN":
            new_head = [self.snake_list[0][0], self.snake_list[0][1] + self.block_size]
        elif self.snake_direction == "LEFT":
            new_head = [self.snake_list[0][0] - self.block_size, self.snake_list[0][1]]
        elif self.snake_direction == "RIGHT":
            new_head = [self.snake_list[0][0] + self.block_size, self.snake_list[0][1]]

        self.snake_list.insert(0, new_head)

        if self.snake_list[0][0] == food.x and self.snake_list[0][1] == food.y:
            self.bite_sound.play()
            food.move()
        else:
            self.snake_list.pop()

        return self.check_collision()

    def draw(self):
        for x in self.snake_list:
            pygame.draw.rect(self.screen, GREEN, [x[0], x[1], self.block_size, self.block_size])

    def check_collision(self):
        if not self.snake_list:
            return True
        if self.snake_list[0][0] >= SCREEN_WIDTH or self.snake_list[0][0] < 0 or self.snake_list[0][1] >= SCREEN_HEIGHT or self.snake_list[0][1] < 0:
            return True

        for x in self.snake_list[1:]:
            if x == self.snake_list[0]:
                return True

        return False

    def check_food_collision(self, food):
        if self.snake_list[0][0] == food.x and self.snake_list[0][1] == food.y:
            self.bite_sound.play()
            return True
        return False
