import pygame
from Player import Player


class game:
    def __init__(self, window):
        self.window = window
        self.player = Player(window)
    