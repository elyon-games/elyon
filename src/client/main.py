import pygame
from client.lib.scrollBar import ScrollBar
from client.lib.title import changeTitle
from client.style.gradient import draw_gradient
import common.path as path
import common.assets as assets
from client.lib.screen.controller import showScreen, updateScreen

BACKGROUND_TOP = (16, 185, 129)  # émeraude
BACKGROUND_BOTTOM = (37, 99, 235)  # Bleu

def InitPygame():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    icon = pygame.image.load(assets.getAsset("/logo/round.ico"))
    pygame.display.set_icon(icon)
    changeTitle("Chargment...")
    window_width, window_height = 800, 600
    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    return window, clock    

def Main(config, options):
    global window, clock
    window, clock = InitPygame()
    changeTitle("Acceuil")

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        window.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            showScreen(window, "auth")
        elif keys[pygame.K_t]:
            showScreen(window, "test")


        updateScreen(window, events)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
