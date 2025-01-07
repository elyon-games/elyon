import pygame

from common.config import getConfig
from common.args import getArgs

pygame.init()
pygame.font.init()
pygame.mixer.init()

from client.lib.title import changeTitle
from client.lib.ping import ping
import common.path as path
import common.assets as assets
from client.style.constants import WHITE
from client.style.fonts import getFont
from client.lib.screen.controller import showScreen, updateScreen

def InitPygame():
    icon = pygame.image.load(assets.getAsset("/logo/round.ico"))
    pygame.display.set_icon(icon)
    changeTitle("Chargment...")
    window_width, window_height = 800, 600
    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    return window, clock

def Main():
    config = getConfig("client")
    options = getArgs()
    global window, clock, ms_per_frame
    ms_per_frame = 10
    window, clock = InitPygame()
    changeTitle("Acceuil")

    print(ping())

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

        updateScreen(window=window, events=events, keys=keys)

        fps = int(clock.get_fps())
        current_ms_per_frame = clock.get_time()
        if abs(current_ms_per_frame - ms_per_frame) >= 5:
            ms_per_frame = current_ms_per_frame
        fps_text = getFont("hud_info").render(f"FPS : {fps}", True, WHITE)
        ms_text = getFont("hud_info").render(f"MSPF : {ms_per_frame}", True, WHITE)
        window.blit(fps_text, (window.get_width() - fps_text.get_width() - 10, 10))
        window.blit(ms_text, (window.get_width() - ms_text.get_width() - 10, 25))

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
