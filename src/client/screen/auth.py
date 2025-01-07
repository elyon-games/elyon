import pygame
from pygame import gfxdraw
from client.style.gradient import draw_gradient
from client.style.constants import EMERAUDE, BLEU, WHITE, BLACK, GRAY
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS
import common.config as config 

class AuthScreen(Screen):
    def __init__(self):
        super().__init__("auth")
        self.username = ""
        self.password = ""
        self.active_input = None
        self.font = pygame.font.Font(None, 32)
        self.button_color = (70, 130, 180)  # Steel blue
        self.button_hover_color = (100, 149, 237)  # Lighter blue
        self.card_color = (40, 40, 40)  # Dark gray for the card
        self.card_border_color = (100, 100, 100)

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

    def render_text_input(self, rect, text, active):
        border_color = WHITE if active else GRAY
        self.draw_rounded_rect(self.surface, rect, BLACK, border_radius=10)
        pygame.draw.rect(self.surface, border_color, rect, 2, border_radius=10)
        text_surface = self.font.render(text, True, WHITE)
        self.surface.blit(text_surface, (rect.x + 10, rect.y + 8))

    def render_button(self, rect, text, hover):
        color = self.button_hover_color if hover else self.button_color
        self.draw_rounded_rect(self.surface, rect, color, border_radius=10)
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.surface.blit(text_surface, text_rect)

    def Update(self, window: pygame.Surface, events: EVENTS, keys: KEYS):
        # Background
        draw_gradient(self.surface, EMERAUDE, BLEU, self.surface.get_width(), self.surface.get_height())

        # Center card dimensions
        card_width, card_height = 400, 300
        card_x = (self.surface.get_width() - card_width) // 2
        card_y = (self.surface.get_height() - card_height) // 2

        # Draw card with rounded corners
        self.draw_rounded_rect(self.surface, (card_x, card_y, card_width, card_height), self.card_color, border_radius=20, border_color=self.card_border_color, border_width=2)

        # Input fields
        username_rect = pygame.Rect(card_x + 50, card_y + 50, 300, 40)
        password_rect = pygame.Rect(card_x + 50, card_y + 110, 300, 40)
        self.render_text_input(username_rect, self.username, self.active_input == "username")
        self.render_text_input(password_rect, "*" * len(self.password), self.active_input == "password")

        # Button
        button_rect = pygame.Rect(card_x + 150, card_y + 200, 100, 40)
        mouse_pos = pygame.mouse.get_pos()
        button_hover = button_rect.collidepoint(mouse_pos)
        self.render_button(button_rect, "Login", button_hover)

        # Handle events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_rect.collidepoint(event.pos):
                    self.active_input = "username"
                elif password_rect.collidepoint(event.pos):
                    self.active_input = "password"
                elif button_rect.collidepoint(event.pos):
                    print(f"Username: {self.username}, Password: {self.password}")  # Process login here
                    self.active_input = None
                else:
                    self.active_input = None
            elif event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    if self.active_input == "username":
                        self.username = self.username[:-1]
                    elif self.active_input == "password":
                        self.password = self.password[:-1]
                elif len(self.username) < 20 and len(self.password) < 20:
                    if self.active_input == "username":
                        self.username += event.unicode
                    elif self.active_input == "password":
                        self.password += event.unicode

        super().Update(window, keys, events)
