import pygame
from client.lib.scrollBar import ScrollBar
from client.lib.title import changeTitle
from client.style.gradient import draw_gradient
import common.path as path

BACKGROUND_TOP = (16, 185, 129) # émeraude
BACKGROUND_BOTTOM = (37, 99, 235)  # Bleu

def Main(config, options):
    pygame.init()
    changeTitle("Acceuil")
    icon = pygame.image.load(f"{path.get_path("assets")}\logo\\round.ico")
    pygame.display.set_icon(icon)
    window_width, window_height = 800, 600
    window = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((0, 0, 0))
        draw_gradient(window, BACKGROUND_TOP, BACKGROUND_BOTTOM, window_width, window_height)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
