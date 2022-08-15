class Settings:
    """Klasa przeznaczona do przechowywania wszystkich ustawień gry."""

    def __init__(self):
        """Inicjalizacja ustawień gry."""
        self.bg_color = (230, 230, 230)
        #Ustawienia dotyczące statku.
        self.ship_limit = 2
        #Ustawienia dotyczące pocisku.
        self.bullet_width = 18
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        #self.lerka_speed = 1.2
        #self.fleet_move_speed_x = 60
        #self.fleet_move_speed_y = 60

        self.speedup_scale = 1.1
        self.speedup_scale_lerka = 0.028

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicjalizacja ustawień, które ulegają zmianie w trakcie gry."""
        self.ship_speed = 1.9
        self.bullet_speed = 3.0
        self.lerka_speed_x = 0.2
        self.lerka_speed_y = 0.2

        self.fleet_direction = 1

    def increase_speed(self):
        """Zmiana ustawień dotyczących szybkości."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.lerka_speed_x += self.speedup_scale_lerka
        self.lerka_speed_y += self.speedup_scale_lerka