import pygame

from jeu_dammier.entite import *

class Player(Entite, pygame.sprite.Sprite) :
    def __init__(self, x, y, screen, tmx_map, objet) -> None:
        Entite.__init__(self, tmx_map)
        pygame.sprite.Sprite.__init__(self)
        print(x,y)
        self.x = x
        self.y = y
        self.alive = True
        self.image = pygame.Surface((32, 32))  
        self.image.fill((0, 255, 0))  
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.dégat = 10
        self.screen = screen
        self.objet = objet
    
    def attaquer(self):
        print(f"j'attaque: -{self.dégat}")

    def vérif_sur_objet(self):
        for obj in self.objet.values():
            dans = self.x > obj["x"] and self.x < obj["x"]+obj["width"] and self.y > obj["y"] and self.y < obj["y"]+obj["height"]
            print(dans)
            if dans:
                print("tes sur un objet 1 ")
                return True 
            else:
                return False 

    