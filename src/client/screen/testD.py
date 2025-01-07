import pygame
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS
from client.style.fonts import getFontSize

class TestScreen(Screen):
    def __init__(self):
        super().__init__("test")
    
    def Update(self, window: pygame.Surface, events: EVENTS, keys: KEYS):

        super().Update(window, keys, events)
