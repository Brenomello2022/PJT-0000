import pygame
import random
from constants import *

class Food:
    def __init__(self, screen, block_size):
        self.screen = screen
        self.block_size = block_size
        self.x = round(random.randrange(0, SCREEN_WIDTH - self.block_size) / self.block_size) * self.block_size
        self.y = round(random.randrange(0, SCREEN_HEIGHT - self.block_size) / self.block_size) * self.block_size
        self.color = random.choice([c for c in COLORS if c != BLACK])
        self.last_color_change = pygame.time.get_ticks()
        self.color_change_interval = 1000

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.block_size, self.block_size])

    def move(self):
        self.x = round(random.randrange(0, SCREEN_WIDTH - self.block_size) / self.block_size) * self.block_size
        self.y = round(random.randrange(0, SCREEN_HEIGHT - self.block_size) / self.block_size) * self.block_size

    def update_color(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change >= self.color_change_interval:
            self.color = random.choice([c for c in COLORS if c != BLACK])
            self.last_color_change = current_time
