import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.var import auth as authData
from client.style.gradient import draw_gradient
from client.lib.assets import getAsset
from client.style.constants import EMERAUDE, BLEU, WHITE, BLACK, GRAY, STEEL_BLUE, LIGHTER_BLUE, CARD_COLOR, CARD_BORDER_COLOR
from client.style.fonts import getFontSize


class SuperSmashMenu(Screen):
    def __init__(self, window):
        super().__init__(window, "home", "Super Smash")
        self.logo = getAsset("logo")
        self.window = window

    def draw_rounded_rect(self, surface, rect, color, border_radius=20, border_color=None, border_width=0):
        """Dessine un rectangle avec des coins arrondis."""
        x, y, w, h = rect
        pygame.draw.rect(surface, color, (x + border_radius, y, w - 2 * border_radius, h))  # Centre
        pygame.draw.rect(surface, color, (x, y + border_radius, w, h - 2 * border_radius))  # Verticales
        pygame.draw.circle(surface, color, (x + border_radius, y + border_radius), border_radius)  # Coin haut gauche
        pygame.draw.circle(surface, color, (x + w - border_radius, y + border_radius), border_radius)  # Coin haut droit
        pygame.draw.circle(surface, color, (x + border_radius, y + h - border_radius), border_radius)  # Coin bas gauche
        pygame.draw.circle(surface, color, (x + w - border_radius, y + h - border_radius), border_radius)  # Coin bas droit

        if border_width > 0 and border_color:
            inner_rect = pygame.Rect(
                x + border_width, y + border_width, w - 2 * border_width, h - 2 * border_width
            )
            self.draw_rounded_rect(surface, inner_rect, border_color, border_radius - border_width)

    def render_button(self, rect, text, hover):
        color = LIGHTER_BLUE if hover else STEEL_BLUE
        self.draw_rounded_rect(self.surface, rect, color, border_radius=10)
        text_surface = getFontSize(32).render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.surface.blit(text_surface, text_rect)

    def UpdateView(self):
        start_button = pygame.Rect(
            (self.window.get_width() / 2) - ((self.window.get_width() / 10) / 2),
            (self.window.get_height() / 2) - ((self.window.get_height() / 10) / 2),
            self.window.get_width() / 10,
            self.window.get_height() / 10,
        )
        self.render_button(start_button, "Start", False)


    def HandleEvent(self, type, event):
        pass