class Settings:
    """Klasa przeznaczona do przechowywania wszystkich ustawień gry."""

    def __init__(self):
        """Inicjalizacja ustawień gry."""
        self.bg_color = (230, 230, 230)

        self.ship_limit = 2

        self.bullet_width = 18
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # self.lerka_speed = 1.2
        # self.fleet_move_speed_x = 60
        # self.fleet_move_speed_y = 60
        self.missleab_width = 5
        self.missleab_height = 18
        self.missleab_color = (60, 60, 60)

        self.speedup_scale = 1.1
        self.speedup_scale_lerka = 0.028
        self.score_scale = 1.5

        self.difficulty_level = 'medium'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicjalizacja ustawień, które ulegają zmianie w trakcie gry."""
        if self.difficulty_level == 'easy':
            self.ship_limit = 4
            self.bullets_allowed = 5
            self.ship_speed = 1.2
            self.bullet_speed = 1.9
            self.missles_speed = 1.0
            self.missles_allowed = 1
            self.lerka_speed_x = 0.09
            self.lerka_speed_y = 0.09
            self.lerka_points = 30
        elif self.difficulty_level == 'medium':
            self.ship_limit = 2
            self.bullets_allowed = 3
            self.ship_speed = 1.9
            self.bullet_speed = 3.0
            self.missles_speed = 2.0
            self.missles_allowed = 2
            self.lerka_speed_x = 0.2
            self.lerka_speed_y = 0.2
            self.lerka_points = 50
        elif self.difficulty_level == 'hard':
            self.ship_limit = 1
            self.bullets_allowed = 3
            self.ship_speed = 3.0
            self.bullet_speed = 8.0
            self.missles_speed = 3.0
            self.missles_allowed = 3
            self.lerka_speed_x = 0.48
            self.lerka_speed_y = 0.48
            self.lerka_points = 80

        self.fleet_direction = 1

    def increase_speed(self):
        """Zmiana ustawień dotyczących szybkości."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.lerka_speed_x += self.speedup_scale_lerka
        self.lerka_speed_y += self.speedup_scale_lerka
        self.lerka_points = int(self.lerka_points * self.score_scale)
