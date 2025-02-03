import pygame
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS
from client.lib.title import changeTitle
from client.lib.me import getData
from client.var import auth as authData

class HomeScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "home", "Accueil")
    
    def UpdateView(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"sa {authData}", True, (255, 255, 255))
        self.surface.blit(text, (10, 10))
