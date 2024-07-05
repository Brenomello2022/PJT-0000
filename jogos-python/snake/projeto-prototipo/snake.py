import pygame
import time
import random

pygame.init()

# Definindo cores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (125, 60, 152)
gray = (140, 136, 139)
lightGray = (221, 216, 219)
pink = (246, 9, 163)
lightPink = (244, 95, 192)
aqua = (31, 221, 218)
orange = (247, 110, 47)
colors = [red, green, yellow, white, blue, purple, gray, lightGray, pink, lightPink, aqua, orange]

# Dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Sons
button_sound = pygame.mixer.Sound("audios/button.wav")
bite_sound = pygame.mixer.Sound("audios/bite.wav")
game_over_sound = pygame.mixer.Sound("audios/game-over.wav")

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

def start_screen():
    start = False
    while not start:
        screen.fill(black)
        title = score_font.render("New Game", True, white)
        title_rect = title.get_rect(center=(screen_width / 2, screen_height / 3))
        screen.blit(title, title_rect.topleft)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(screen_width / 2 - 50, screen_height / 2 - 25, 100, 50)
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, red, button_rect)
            if click[0] == 1:
                button_sound.play()
                time.sleep(0.5)
                start = True
        else:
            pygame.draw.rect(screen, green, button_rect)

        start_text = font_style.render("Start", True, white)
        start_text_rect = start_text.get_rect(center=button_rect.center)
        screen.blit(start_text, start_text_rect.topleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def game_over_screen():
    game_over = False
    game_over_sound.play()
    while not game_over:
        screen.fill(black)
        title = score_font.render("Game Over", True, white)
        title_rect = title.get_rect(center=(screen_width / 2, screen_height / 3))
        screen.blit(title, title_rect.topleft)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        button_rect = pygame.Rect(screen_width / 2 - 75, screen_height / 2 - 25, 150, 50)
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, red, button_rect)
            if click[0] == 1:
                button_sound.play()
                time.sleep(0.5)
                gameLoop()
        else:
            pygame.draw.rect(screen, green, button_rect)

        play_again_text = font_style.render("Play Again", True, white)
        play_again_text_rect = play_again_text.get_rect(center=button_rect.center)
        screen.blit(play_again_text, play_again_text_rect.topleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def gameLoop():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    food_color = random.choice([color for color in colors if color != blue])  # Escolhe uma cor diferente de blue

    last_color_change_time = time.time()

    while not game_over:

        while game_close == True:
            game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(black)

        current_time = time.time()
        if current_time - last_color_change_time >= 1:
            food_color = random.choice([color for color in colors if color != blue])  # Escolhe uma cor diferente de blue
            last_color_change_time = current_time

        pygame.draw.rect(screen, food_color, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            bite_sound.play()
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

start_screen()
gameLoop()
