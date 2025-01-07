import pygame
from client.types import EVENTS, KEYS, EVENT
class Screen():
    def __init__(self, id):
        self.id = id
        self.window = None
        self.surface = None
        self.isMounted = False

    def updateSurface(self, size):
        self.surface = pygame.Surface(size, pygame.RESIZABLE)

    def getSize(self):
        if self.window is None:
            return (0, 0)
        return self.window.get_size()

    def Mount(self, window: pygame.Surface):
        self.window = window
        self.updateSurface(self.getSize())
        self.isMounted = True

    def UnMount(self):
        self.surface = None
        self.isMounted = False

    def Update(self, window: pygame.Surface, events: EVENTS, keys: KEYS):
        if self.isMounted:
            self.window = window
            self.window.blit(self.surface, (0, 0), self.surface.get_rect())

    def HandleEvent(self, type: int, event: EVENT):
        pass

    def calculate_position(self, percentage_x, percentage_y, size_x=0, size_y=0):
        x = int(self.surface.get_width() * (percentage_x / 100) - size_x / 2)
        y = int(self.surface.get_height() * (percentage_y / 100) - size_y / 2)
        return x, y