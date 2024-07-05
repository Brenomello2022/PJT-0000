import pygame
from constants import *

class Button:
    def __init__(self, screen, text, x, y, width, height):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, RED, button_rect)
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, GREEN, button_rect)

        text_render = pygame.font.SysFont("comicsansms", 20).render(self.text, True, WHITE)
        text_rect = text_render.get_rect(center=button_rect.center)
        self.screen.blit(text_render, text_rect.topleft)

        return False
