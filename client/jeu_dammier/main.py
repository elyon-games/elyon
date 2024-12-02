import pygame
import pytmx
import pyscroll
import time

from jeu_dammier.player import *
from jeu_dammier.entite import *

class Game:
    def __init__(self) -> None:
        self.object = {}

        self.mob = {}
    
        self.font = pygame.font.SysFont("Arial", 24)

        self.screen =pygame.display.set_mode((700, 700))

        tmx_map = pytmx.util_pygame.load_pygame('jeu_dammier/assets/map/sans titre.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_map)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2.8

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)

        self.récupérer_objet(tmx_map)

        self.spawn = tmx_map.get_object_by_name('spawn')
        self.player = Player(self.spawn.x, self.spawn.y, self.screen,  tmx_map, self.object)
        self.group.add(self.player)


    def récupérer_objet(self, tmx_map):
        for obj in tmx_map.objects:
            print(f"Objet: {obj.name}, Type: {obj.type}, Position: (x:{obj.x}, y:{obj.y}), size(width:{obj.width}, height:{obj.height})")
            if obj.type == "objet":
                self.object.update({obj.name: 
                                    {"x": int(obj.x) , "y" : int(obj.y), 
                                     "width":int(obj.width), "height":int(obj.height)
                                    }
                                    })
                print(self.object)


    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.avancer()
        if pressed[pygame.K_DOWN]:
            self.player.bas()
        if pressed[pygame.K_RIGHT]:
            self.player.droite()
        if pressed[pygame.K_LEFT]:
            self.player.gauche()
        objet = self.player.vérif_sur_objet()
        if objet:
            print("tes sur un objet")

        if pressed[pygame.K_SPACE]:
            self.player.attaquer()
        

    def sur_objet(self):
        if True:
            self.player.récupérer_object("épée")

    def create_mob(self):
        self.mob = {}

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            self.handle_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.group.center(self.player.rect.center)
            self.group.update()
            self.group.draw(self.screen)

            text= self.font.render(f"x: {self.player.x}; y: {self.player.y} ", True, "RED")
            self.screen.blit(text,(0,0))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
    
def main():
    pygame.init()
    game=Game()
    game.run()