import pygame
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS
from client.style.fonts import getFontSize
from client.lib.title import changeTitle

class TestScreen(Screen):
    def __init__(self):
        super().__init__("test")
    
    def Update(self, window: pygame.Surface, events: EVENTS, keys: KEYS):
        print("sa")
        changeTitle("test")

        super().Update(window, keys, events)
