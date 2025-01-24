import pygame
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS

class HomeScreen(Screen):
    def __init__(self):
        super().__init__("home")
    
    def Update(self, window: pygame.Surface, events: EVENTS, keys: KEYS):
        super().Update(window, keys, events)
