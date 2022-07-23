import pygame

class Ship:
    """Klasa przeznaczona do zarządzania statkiem kosmicznym."""

    def __init__(self, li_game):
        """Inicjalizacja statku kosmicznego i jego położenie początkowe."""

        self.screen = li_game.screen
        self.settings = li_game.settings
        self.screen_rect = li_game.screen.get_rect()

        #Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Każdy nowy statek kosmiczny pojawia się na środku ekranu.
        self.rect.midleft = self.screen_rect.midleft

        #Położenie pionowe statku jest przechowywane w postaci
        # liczby zmiennoprzecinkowej.
        self.y = float(self.rect.y)

        #Opcje wskazujące na poruszanie się statku.
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """
        Uaktualnienie położenia statku na podstawie opcji wskazującej
        na jego ruch.
        """
        #Uaktualnienie wartości współrzędnej Y statku, a nie jego prostokąta.
        if self.moving_up and self.rect.top > 2:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        #Uaktualnienie obiektu rect na podstawie wartości self.y.
        self.rect.y = self.y


    def blitme(self):
        """Wyświetla statek kosmiczny w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)