import pygame
from typing import List
import client.lib.screen.base as Screen
from client.screen.auth import AuthScreen
from client.screen.testD import TestScreen

actualScreen = None

screens = {
    "auth": AuthScreen,
    "test": TestScreen
}

def UnMountScreen():
    global actualScreen
    if actualScreen is not None and actualScreen.isMounted:
        actualScreen.UnMount()
        actualScreen = None

def showScreen(window: pygame.Surface, screen: str) -> Screen:
    global actualScreen
    if actualScreen is not None and actualScreen.id == screen:
        return actualScreen
    elif actualScreen is None or actualScreen.id != screen:
        UnMountScreen()
        actualScreen = screens[screen]()
        actualScreen.Mount(window)
    else:
        raise Exception(f"Screen {screen} not found.")
    
    return actualScreen

def updateScreen(window: pygame.Surface, events: List[pygame.event.EventType]):
    global actualScreen
    if actualScreen is not None and actualScreen.isMounted:
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                actualScreen.updateSurface((event.w, event.h))
            actualScreen.HandleEvent(type=event.type, event=event)
        actualScreen.Update(window)
