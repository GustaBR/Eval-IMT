import pygame
import os

def lerp(a, b, t):
    return a + (b - a) * t

def blend_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def load_icon(caminho, tamanho):
    if os.path.isfile(caminho):
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.smoothscale(img, (tamanho, tamanho))
    return None