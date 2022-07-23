import pygame
from pygame.sprite import Sprite

class Lerka(Sprite):
    """Klasa przedstawiająca jednego Lerkę we flocie."""

    def __init__(self, li_game):
        """Inicjalizacja Lerki i zdefiniowanie jego położenia."""
        super().__init__()
        self.screen = li_game.screen
        self.settings = li_game.settings
        self.screen_rect = li_game.screen.get_rect()

        self.image = pygame.image.load('images/lerka.bmp')
        self.rect = self.image.get_rect()

        self.rect.topright = self.screen_rect.topright
        self.y = self.rect.y


