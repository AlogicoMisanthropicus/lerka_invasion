import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from lerka import Lerka

class LerkaInvasion:
    """
    Ogólna klasa przeznaczona do zarządzania zasobami i sposobem 
    działania gry.
    """

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobów."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("LERKA Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.lerkas = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Rozpoczęcie pętli głównej gry."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_lerka()
            self._update_screen()

    def _check_events(self):
        """Reakcja na zdarzenia generowane przez klawiaturę i mysz."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Reakcja na naciśnięcie klawisza."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Reakcja na zwolnienie klawisza."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Utworzenie nowego pocisku i dodanie go do grupy pocisków."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """
        Uaktualnienie położenia pocisków i usunięcie tych niewidocznych
         na ekranie.
        """
        #Uaktualnienie położenia pocisków.
        self.bullets.update()

        #Usunięcie pocisków, które znajdują się poza ekranem.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_lerka_collisions()

    def _check_bullet_lerka_collisions(self):
        """Reakcja na kolizję między pociskiem a Lerką."""
        #Usunięcie wszystkich pocisków i Lerków, między którymi doszło 
        #do kolizji.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.lerkas, True, True)

        if not self.lerkas:
            #Pozbycie się istniejących pocisków i utworzenie nowej floty.
            self.bullets.empty()
            self._create_fleet()

    def _update_lerka(self):
        """Uaktualnienie położenia wszystkich obcych we flocie."""
        self._check_fleet_edges()
        self.lerkas.update()

    def _create_fleet(self):
        """Utworzenie pełnej floty Lerków."""
        lerka = Lerka(self)
        lerka_height, lerka_width = lerka.rect.size
        available_space_y = self.settings.screen_height - lerka_height
        number_lerkas_y = available_space_y // (2 * lerka_height)

        ship_width = self.ship.rect.width
        available_space_x = (self.settings.screen_width -
            (2 * lerka_width) - ship_width)
        number_rows = available_space_x // (2 * lerka_width)

        for row_number in range(number_rows):
            for lerka_number in range(number_lerkas_y):
                self._create_lerka(lerka_number, row_number)

    def _create_lerka(self, lerka_number, row_number):
        """Utworzenie Lerki i umieszczenie go w rzędzie."""
        lerka = Lerka(self)
        lerka_height, lerka_width = lerka.rect.size
        #lerka.y = (lerka_height + 2 * lerka_height * lerka_number)
        #lerka.y = (2 * lerka_height * lerka_number + random_number)
        lerka.y = lerka_height + 2 * lerka_height * lerka_number
        lerka.rect.y = lerka.y
        lerka.x = ((self.settings.screen_width + 5 * lerka.rect.width)
            - 2 * lerka.rect.width * row_number)
        lerka.rect.x = lerka.x
        self.lerkas.add(lerka)

    def _check_fleet_edges(self):
        """Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu."""
        for lerka in self.lerkas.sprites():
            if lerka.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Zmiana kierunku floty."""
        for lerka in self.lerkas.sprites():
            lerka.rect.x -= self.settings.fleet_move_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu."""
        #Odświeżenie ekranu w trakcie każdej iteracji pętli.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.lerkas.draw(self.screen)

        #Wyświetelenie ostatnio zmodyfikowanego ekranu.
        pygame.display.flip()

if __name__ == '__main__':
    li = LerkaInvasion()
    li.run_game()