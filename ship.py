import pygame

class Ship():
    """Klasa przeznaczona do zarządzania statkiem kosmicznym."""

    def __init__(self, li_game):
        """Inicjalizacja statku kosmicznego i jego położenie początkowe."""

        self.screen = li_game.screen
        self.screen_rect = li_game.screen.get_rect()

        #Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Każdy nowy statek kosmiczny pojawia się na środku ekranu.
        self.rect.midleft = self.screen_rect.midleft

    def blitme(self):
        """Wyświetla statek kosmiczny w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)