import pygame
from client.style.gradient import draw_gradient
from client.lib.screen.base import Screen

class AuthScreen(Screen):
    def __init__(self):
        super().__init__("auth")
    
    def Update(self, window: pygame.Surface):
        draw_gradient(self.surface, (16, 185, 129), (37, 99, 235), self.surface.get_width(), self.surface.get_height())
        self.surface.fill((0, 0, 0), pygame.Rect(self.surface.get_width() // 2 - 50, self.surface.get_height() // 2 - 50, 100, 100))
        super().Update(window)
