import pygame 
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from jeu_dammier.main import main as dammier
from nombre_mystère.nombre_mystère import menu as nb_mystère
from function_menu import *

def menu(screen, font)-> dict:
    menu={
        "titre": font.render(
            "Mon titre",
              True, 
              (255, 255, 255)
            ),
        "bouton_dammier": Button(
            screen, 
            300,
            300,
            300,
            150, 
            text='dammier',
            fontSize=40,
            onClick=lambda: dammier()
        ), 
        "bouton_nb_mystère": Button(
            screen,
            150,
            300,
            300,
            150,
            text="nomber mystère",
            onClick=lambda: nb_mystère()
        )
    }
    
    return menu

def Main()-> None:
    pygame.init()
    font = pygame.font.Font(None, 80)
    screen = pygame.display.set_mode((700,700))
    screen_menu = menu(screen, font)

    titre = screen_menu["titre"].get_rect(center=(150,90))

    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((0,0,0))
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(screen_menu["titre"], titre)

        pygame_widgets.update(events)
        
        for i in screen_menu:
            print(i)

        screen_menu["bouton_dammier"].draw()


        pygame.display.update()
        clock.tick(60)

    pygame.quit()
Main()