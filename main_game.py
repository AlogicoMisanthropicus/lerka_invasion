import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
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

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.lerkas = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "LERKA Invasion")

    def run_game(self):
        """Rozpoczęcie pętli głównej gry."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_lerkas()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Rozpoczęcie nowej gry po kliknięciu przycisku."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
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
        elif event.key == pygame.K_g:
            if not self.stats.game_active:
                self._start_game()
    def _check_keyup_events(self, event):
        """Reakcja na zwolnienie klawisza."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.lerkas.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)
        self.settings.initialize_dynamic_settings()

    def _fire_bullet(self):
        """Utworzenie nowego pocisku i dodanie go do grupy pocisków."""
        if len(self.bullets) < self.settings.bullets_allowed and (
            self.stats.game_active):
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

        #Ćwiczenie 13.6 (s. 361 ) - trafienia Lerków:
        #if collisions:
        #    self.stats.lerka_hit += 1
        #    print(f"Trafiono {self.stats.lerka_hit} Lerków!")

        if not self.lerkas:
            #Pozbycie się istniejących pocisków i utworzenie nowej floty.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
 
    def _update_lerkas(self):
        """Uaktualnienie położenia wszystkich obcych we flocie."""
        self._check_fleet_edges()
        self.lerkas.update()
        #Wykrywanie kolizji między Lerką a statkiem.
        if pygame.sprite.spritecollideany(self.ship, self.lerkas):
            self._ship_hit()

        self._check_lerkas_left_scr()

    def _create_fleet(self):
        """Utworzenie pełnej floty Lerków."""
        lerka = Lerka(self)
        lerka_height, lerka_width = lerka.rect.size
        available_space_y = self.settings.screen_height - 2 * lerka_height
        number_lerkas_y = available_space_y // (2 * lerka_height)

        ship_width = self.ship.rect.width
        available_space_x = (self.settings.screen_width -
            (5 * lerka_width) - ship_width)
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
            lerka.rect.y -= self.settings.lerka_speed_y
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Reakcja na uderzenie Lerki w statek."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.lerkas.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.8)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_lerkas_left_scr(self):
        screen_rect = self.screen.get_rect()
        for lerka in self.lerkas.sprites():
            if lerka.rect.left <= (screen_rect.left - 0.5 * lerka.rect.height):
                self._ship_hit()
                break

    def _update_screen(self):
        """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu."""
        #Odświeżenie ekranu w trakcie każdej iteracji pętli.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.lerkas.draw(self.screen)

        if not self.stats.game_active:
            self.play_button.draw_button()

        #Wyświetelenie ostatnio zmodyfikowanego ekranu.
        pygame.display.flip()

if __name__ == '__main__':
    li = LerkaInvasion()
    li.run_game()