import pygame

global username
username = None

def setUsername(usernameSet) -> None:
    global username
    username = usernameSet

def changeTitle(title) -> None:
    if username :
        pygame.display.set_caption(f"Elyon Client ({username}) - {title}")
    else: 
        pygame.display.set_caption(f"Elyon Client - {title}")
