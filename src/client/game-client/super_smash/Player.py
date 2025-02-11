import pygame

class Player:
    def __init__(self, window):
        self.window = window
        self.rect = pygame.Rect(100, self.window.get_height() - 100, 50, 50)
        self.vitesse_y = 0
        self.au_sol = False

    def deplacer(self, touches):
        if touches[pygame.K_LEFT]:
            self.rect.x -= 5
        if touches[pygame.K_RIGHT]:
            self.rect.x += 5
        if touches[pygame.K_SPACE] and self.au_sol:
            self.vitesse_y = -10
            self.au_sol = False

    def appliquer_gravite(self):
        self.vitesse_y += 0.5
        self.rect.y += self.vitesse_y
        if self.rect.y >= self.window.get_height() - 50:
            self.rect.y = self.window.get_height() - 50
            self.au_sol = True
            self.vitesse_y = 0

    def afficher(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)