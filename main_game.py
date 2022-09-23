import sys
from time import sleep
import json

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from missle_a import MissleA
from missle_b import MissleB
from lerka import Lerka
from help import Help

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
        self.sb = Scoreboard(self)
        self.help = Help(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.lerkas = pygame.sprite.Group()
        self.missles_a = pygame.sprite.Group()
        self.missles_b = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "LERKA Invasion")

        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Stwarza przyciski do wyboru poziomu trudności."""
        self.easy_button = Button(self, "Łatwy")
        self.medium_button = Button(self, "Średni")
        self.hard_button = Button(self, "Piekło")
        self.help_button = Button(self, "Pomoc")

        self.easy_button.rect.top = (
            self.play_button.rect.top + 2.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (
            self.easy_button.rect.top + 1.5*self.play_button.rect.height)
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = (
            self.medium_button.rect.top + 1.5*self.play_button.rect.height)
        self.hard_button._update_msg_position()

        self.help_button.rect.bottom = (
            self.play_button.rect.top - 1.5*self.play_button.rect.height)
        self.help_button._update_msg_position()

    def run_game(self):
        """Rozpoczęcie pętli głównej gry."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_lerkas()
                self._update_missles_a()
                self._update_missles_b()

            self._update_screen()
   
    def _check_events(self):
        """Reakcja na zdarzenia klawiatura/mysz."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)
                self._check_help_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Rozpoczęcie nowej gry po kliknięciu przycisku."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Ustawienie wybranego poziomu trudności."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
        elif medium_button_clicked:
            self.settings.difficulty_level = 'medium'
        elif hard_button_clicked:
            self.settings.difficulty_level = 'hard'

    def _check_help_button(self, mouse_pos):
        help_button_clicked = self.help_button.rect.collidepoint(mouse_pos)
        if help_button_clicked:
            if not self.stats.show_help:
                self.stats.show_help = True
            elif self.stats.show_help:
                self.stats.show_help = False
        
    def _create_help_window(self):
        self.help.show_help_window()

    def _check_keydown_events(self, event):
        """Reakcja na naciśnięcie klawisza."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            self._exit_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_LCTRL:
            self._fire_missle_a()
            self._fire_missle_b()
        elif event.key == pygame.K_g:
            if not self.stats.game_active:
                self._start_game()
    def _check_keyup_events(self, event):
        """Reakcja na zwolnienie klawisza."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.show_help = False
        self.sb.prep_images()
        self._emptying_all_bullets_lerkas()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

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
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.lerkas, True, True)
        self._when_collisions(collisions)
        self._lerkas_end()

    def _fire_missle_a(self):
        """Utworzenie nowego pocisku A i dodanie go do grupy pocisków A."""
        if len(self.missles_a) < self.settings.missles_allowed and (
            self.stats.game_active):
            new_misslea = MissleA(self)
            self.missles_a.add(new_misslea)

    def _update_missles_a(self):
        """Uaktualnienie położenia pocisków A i usunięcie niewidocznych 
        na ekranie."""
        self.missles_a.update()

        for misslea in self.missles_a.copy():
            if misslea.rect.bottom <= 0:
                self.missles_a.remove(misslea)

        self._check_misslea_lerka_collisions()

    def _check_misslea_lerka_collisions(self):
        """Reakcja na kolizję między pociskiem A i Lerką."""
        collisions = pygame.sprite.groupcollide(
            self.missles_a, self.lerkas, True, True)
        self._when_collisions(collisions)
        self._lerkas_end()

    def _fire_missle_b(self):
        """Utworzenie nowego pocisku B i dodanie go do grupy pocisków B."""
        if len(self.missles_b) < self.settings.missles_allowed and (
            self.stats.game_active):
            new_missleb = MissleB(self)
            self.missles_b.add(new_missleb)

    def _update_missles_b(self):
        """Uaktualnienie położenia pocisków B i usunięcie niewidocznych 
        na ekranie."""
        self.missles_b.update()

        for missleb in self.missles_b.copy():
            if missleb.rect.top >= self.settings.screen_height:
                self.missles_b.remove(missleb)

        self._check_missleb_lerka_collisions()

    def _check_missleb_lerka_collisions(self):
        """Reakcja na kolizję między pociskiem B i Lerką."""
        collisions = pygame.sprite.groupcollide(
            self.missles_b, self.lerkas, True, True)
        self._when_collisions(collisions)
        self._lerkas_end()

    def _when_collisions(self, collision):
        collisions = collision

        if collisions:
            for lerkas in collisions.values():
                self.stats.score += self.settings.lerka_points * len(lerkas)
            self.sb.prep_score()
            self.sb.check_high_score()
 
    def _update_lerkas(self):
        """Uaktualnienie położenia wszystkich obcych we flocie."""
        self._check_fleet_edges()
        self.lerkas.update()
        #Wykrywanie kolizji między Lerką a statkiem.
        if pygame.sprite.spritecollideany(self.ship, self.lerkas):
            self._ship_hit()

        self._check_lerkas_left_scr()

    def _emptying_all_bullets_lerkas(self):
        self.lerkas.empty()
        self.bullets.empty()
        self.missles_a.empty()
        self.missles_b.empty()

    def _lerkas_end(self):
        """Działania po zestrzeleniu floty Lerków: pozbycie się pocisków, 
        tworzenie nowej floty, zwiększenie prędkości i poziomu etc."""
        if not self.lerkas:
            #Pozbycie się istniejących pocisków i utworzenie nowej floty.
            self.bullets.empty()
            self.missles_a.empty()
            self.missles_b.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

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
            self.sb.prep_ships()
            self.lerkas.empty()
            self.bullets.empty()
            self.missles_a.empty()
            self.missles_b.empty()
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

    def _exit_game(self):
        """Zapisuje najlepszy wynik i zamyka grę."""
        old_high_score = self.stats.get_old_high_score()
        if self.stats.high_score > old_high_score:
            with open('high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)

        sys.exit()

    def _update_screen(self):
        """Uaktualnienie obrazów na ekranie i przejście do nowego ekranu."""
        #Odświeżenie ekranu w trakcie każdej iteracji pętli.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for misslea in self.missles_a.sprites():
            misslea.draw_misslea()
        for missleb in self.missles_b.sprites():
            missleb.draw_missleb()
        self.lerkas.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.help_button.draw_button()
            if self.stats.show_help:
                self._create_help_window()

        #Wyświetelenie ostatnio zmodyfikowanego ekranu.
        pygame.display.flip()

if __name__ == '__main__':
    li = LerkaInvasion()
    li.run_game()