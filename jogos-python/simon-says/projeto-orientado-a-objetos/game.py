import pygame
import random
from settings import *

class Game:
    def __init__(self):
        self.sequence = []
        self.player_sequence = []
        self.game_over = False
        self.running = True
        self.showing_sequence = False
        self.level = 0
        self.color_rects = []
        self.confirm_exit = False
        self.create_color_rects()

    def create_color_rects(self):
        if self.level == 0:
            self.color_rects = [
                pygame.Rect(0, 0, screen_width // 2, screen_height // 2),
                pygame.Rect(screen_width // 2, 0, screen_width // 2, screen_height // 2),
                pygame.Rect(0, screen_height // 2, screen_width // 2, screen_height // 2),
                pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 2)
            ]
        elif self.level == 1:
            self.color_rects = [
                pygame.Rect(x, y, screen_width // 3, screen_height // 3)
                for y in range(0, screen_height, screen_height // 3)
                for x in range(0, screen_width, screen_width // 3)
            ]
        elif self.level == 2:
            self.color_rects = [
                pygame.Rect(x, y, screen_width // 4, screen_height // 4)
                for y in range(0, screen_height, screen_height // 4)
                for x in range(0, screen_width, screen_width // 4)
            ]
        elif self.level == 3:
            self.color_rects = [
                pygame.Rect(x, y, screen_width // 5, screen_height // 5)
                for y in range(0, screen_height, screen_height // 5)
                for x in range(0, screen_width, screen_width // 5)
            ]

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def start_screen(self):
        while self.running and not self.confirm_exit:
            screen.fill(black)
            self.draw_text('Welcome! Choose a Level', score_font, white, screen, screen_width // 2, screen_height // 2 - 150)

            buttons = [
                ('Easy', pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 60, 200, 50)),
                ('Moderate', pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)),
                ('Challenging', pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)),
                ('Hard', pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 120, 200, 50))
            ]

            mouse_pos = pygame.mouse.get_pos()
            for text, rect in buttons:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, green, rect)
                else:
                    pygame.draw.rect(screen, red, rect)
                self.draw_text(text, font_style, black, screen, rect.centerx, rect.centery)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.confirm_exit = True
                    self.confirm_exit_screen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, (text, rect) in enumerate(buttons):
                        if rect.collidepoint(event.pos):
                            button_sound.play()
                            self.level = i
                            self.start_game(i)
                            return True

    def start_game(self, level):
        self.level = level
        self.create_color_rects()
        self.sequence = [random.randint(0, len(self.color_rects) - 1)]
        self.player_sequence = []
        self.show_sequence()

    def game_screen(self):
        while self.running and not self.game_over and not self.confirm_exit:
            screen.fill(black)
            for i, rect in enumerate(self.color_rects):
                pygame.draw.rect(screen, colors[self.level][i % len(colors[self.level])], rect)

            for rect in self.color_rects:
                pygame.draw.rect(screen, white, rect, 5)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.confirm_exit = True
                    self.confirm_exit_screen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.showing_sequence:
                        pos = pygame.mouse.get_pos()
                        for i, rect in enumerate(self.color_rects):
                            if rect.collidepoint(pos):
                                self.player_sequence.append(i)

                                if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
                                    wrong_sound.play()
                                    self.game_over = True
                                    self.game_over_screen()
                                else:
                                    if len(self.player_sequence) == len(self.sequence):
                                        correct_sound.play()
                                        self.player_sequence = []
                                        self.sequence.append(random.randint(0, len(self.color_rects) - 1))
                                        self.show_sequence()

            if self.game_over:
                self.game_over_screen()

    def game_over_screen(self):
        while self.game_over and not self.confirm_exit:
            screen.fill(black)
            self.draw_text('Game Over', score_font, white, screen, screen_width // 2, screen_height // 2 - 150)

            play_again_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
            mouse_pos = pygame.mouse.get_pos()
            if play_again_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, green, play_again_button)
            else:
                pygame.draw.rect(screen, red, play_again_button)
            self.draw_text('Play Again', font_style, black, screen, play_again_button.centerx, play_again_button.centery)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.confirm_exit = True
                    self.confirm_exit_screen()
                if event.type == pygame.MOUSEBUTTONDOWN and play_again_button.collidepoint(event.pos):
                    button_sound.play()
                    self.game_over = False
                    self.start_screen()

    def confirm_exit_screen(self):
        while self.confirm_exit:
            screen.fill(black)
            self.draw_text('Tem certeza que deseja sair?', score_font, white, screen, screen_width // 2, screen_height // 4)

            no_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2, 100, 50)
            yes_button = pygame.Rect(screen_width // 2 + 50, screen_height // 2, 100, 50)

            mouse_pos = pygame.mouse.get_pos()

            if no_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, green, no_button)
            else:
                pygame.draw.rect(screen, red, no_button)
            self.draw_text('Não', font_style, black, screen, no_button.centerx, no_button.centery)

            if yes_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, green, yes_button)
            else:
                pygame.draw.rect(screen, red, yes_button)
            self.draw_text('Sim', font_style, black, screen, yes_button.centerx, yes_button.centery)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.confirm_exit = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if no_button.collidepoint(event.pos):
                        button_sound.play()
                        self.confirm_exit = False
                    if yes_button.collidepoint(event.pos):
                        button_sound.play()
                        self.running = False
                        self.confirm_exit = False
                        self.game_over = False

    def show_sequence(self):
        self.showing_sequence = True
        for i in self.sequence:
            screen.fill(black)
            pygame.draw.rect(screen, colors[self.level][i % len(colors[self.level])], self.color_rects[i])
            pygame.display.flip()
            pygame.time.wait(800)
            screen.fill(black)
            pygame.display.flip()
            pygame.time.wait(300)
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        self.showing_sequence = False

    def run(self):
        while self.running:
            if self.start_screen():
                self.game_screen()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Simon Says')
    
    game = Game()
    game.run()
    
    pygame.quit()
    print("Player has quit the game.")
