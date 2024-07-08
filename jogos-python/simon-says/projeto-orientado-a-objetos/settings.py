import pygame

# Inicializar o Pygame.
pygame.init()

# Definir as dimensões da tela.
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simon Says')

# Definir as cores para a as telas e botões.
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Cores para o nível 'Easy'.
easy_colors = [
    (0, 0, 255),  # BLUE
    (0, 128, 0),  # GREEN
    (255, 0, 0),  # RED
    (255, 255, 0) # YELLOW
]

# Cores para o nível 'Moderate'.
moderate_colors = [
    (0, 255, 255),  # AQUA
    (0, 0, 255),    # BLUE
    (139, 69, 19),  # BROWN
    (0, 128, 0),    # GREEN
    (255, 165, 0),  # ORANGE
    (128, 0, 128),  # PURPLE
    (255, 0, 0),    # RED
    (192, 192, 192),# SILVER
    (255, 255, 0)   # YELLOW
]

# Cores para o nível 'Challenging'.
challenging_colors = [
    (0, 255, 255),  # AQUA
    (0, 0, 255),    # BLUE
    (139, 69, 19),  # BROWN
    (0, 0, 139),    # DARK_BLUE
    (139, 0, 0),    # DARK_RED
    (128, 128, 128),# GRAY
    (0, 128, 0),    # GREEN
    (0, 191, 255),  # LIGHT_BLUE
    (0, 255, 0),    # LIGHT_GREEN
    (255, 0, 255),  # MAGENTA
    (255, 165, 0),  # ORANGE
    (255, 20, 147), # PINK
    (128, 0, 128),  # PURPLE
    (255, 0, 0),    # RED
    (192, 192, 192),# SILVER
    (255, 255, 0)   # YELLOW
]

# Cores para o nível 'Hard'.
hard_colors = [
    (0, 255, 255),  # AQUA
    (127, 255, 212),# AQUAMARINE
    (0, 0, 255),    # BLUE
    (139, 69, 19),  # BROWN
    (248, 131, 121),# CORAL
    (0, 0, 139),    # DARK_BLUE
    (92, 64, 51),   # DARK_BROWN
    (204, 85, 0),   # DARK_ORANGE
    (139, 0, 0),    # DARK_RED
    (139, 128, 0),  # DARK_YELLOW
    (255, 215, 0),  # GOLD
    (128, 128, 128),# GRAY
    (0, 128, 0),    # GREEN
    (0, 163, 108),  # JADE
    (115, 79, 150), # LAVENDER
    (0, 191, 255),  # LIGHT_BLUE
    (0, 255, 0),    # LIGHT_GREEN
    (255, 0, 255),  # MAGENTA
    (255, 165, 0),  # ORANGE
    (255, 20, 147), # PINK
    (128, 0, 128),  # PURPLE
    (255, 0, 0),    # RED
    (192, 192, 192),# SILVER
    (148, 0, 211),  # VIOLET
    (255, 255, 0)   # YELLOW
]

# Mapeando as cores para cada nível.
colors = [easy_colors, moderate_colors, challenging_colors, hard_colors]

# Carregar os sons.
button_sound = pygame.mixer.Sound('audios/button.wav')
correct_sound = pygame.mixer.Sound('audios/correct.wav')
wrong_sound = pygame.mixer.Sound('audios/wrong.wav')

# Definir as fontes.
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
