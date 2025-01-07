import pygame
from client.style.gradient import draw_gradient
from client.style.constants import EMERAUDE, BLEU
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS, CLOCK

class AuthScreen(Screen):
    def __init__(self):
        super().__init__("auth")
    
    def Update(self, window: pygame.Surface, events: EVENTS, keys: KEYS, options: dict, config: dict, clock: CLOCK):
        draw_gradient(self.surface, EMERAUDE, BLEU, self.surface.get_width(), self.surface.get_height())
        super().Update(window, keys, events, options, config, clock)
