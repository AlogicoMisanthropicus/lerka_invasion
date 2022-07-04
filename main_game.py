import sys

import pygame

class LerkaInvasion():
    """
    Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania
    gry.
    """

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobów."""
        pygame.init()

        self.screen = pygame.display.set_mode((1500, 900))
        pygame.display.set_caption("LERKA Invasion")

    def run_game(self):
        