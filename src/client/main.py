import pygame 
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from client.jeu_dammier.main import main as dammier
from client.nombre_mystère.nombre_mystère import menu as nb_mystere
from function_menu import *

def menu(screen, font)-> dict:
    menu={
        "titre": font.render(
            "Mon titre",
              True, 
              (255, 255, 255)
            ), "bouton":{
                "bouton_dammier": Button(
                    screen, 
                    0,
                    100,
                    100,
                    100, 
                    text='dammier',
                    fontSize=40,
                    onClick=lambda: dammier()
                ), 
                "bouton_nb_mystère": Button(
                    screen,
                    100,
                    100,
                    100,
                    100,
                    text="nomber mystère",
                    onClick=lambda: nb_mystere()
                ), "bouton_pendu": Button(
                    screen,
                    200,
                    100,
                    100,
                    100,
                    text="pendu",
                    onClick=pendu
                )
            }
    }
    
    return menu

def pendu():
    print("pendu")

def Main()-> None:
    pygame.init()
    font = pygame.font.Font(None, 80)
    screen = pygame.display.set_mode((700,700))
    screen_menu = menu(screen, font)
    print(screen_menu)
    
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((0,0,0))
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        for i in screen_menu.keys():
            if i != "bouton":
                screen.blit(screen_menu[i], screen_menu[i].get_rect(center=(0,0)))
            else :
                for y in screen_menu[i].values():
                    print("y :",y)
                    y.draw()

        pygame_widgets.update(events)
        
        for i in screen_menu:
            print(i)


        pygame.display.update()
        clock.tick(60)

    pygame.quit()
Main()