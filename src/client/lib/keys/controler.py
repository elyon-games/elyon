import pygame

keys = None

def getKeys():
    global keys
    return keys

def updateKeys(keysSet):
    global keys
    keys = keysSet
