class Settings:
    """Klasa przeznaczona do przechowywania wszystkich ustawień gry."""

    def __init__(self):
        """Inicjalizacja ustawień gry."""
        self.screen_width = 1800
        self.screen_height = 900
        self.bg_color = (230, 230, 230)
        #Ustawienia dotyczące statku.
        self.ship_speed = 1.9
        self.ship_limit = 2
        #Ustawienia dotyczące pocisku.
        self.bullet_speed = 1.9
        self.bullet_width = 20
        self.bullet_height = 8
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.lerka_speed_x = 0.3
        self.lerka_speed_y = 0.4
        #self.lerka_speed = 1.2
        #self.fleet_move_speed_x = 60
        #self.fleet_move_speed_y = 60
        self.fleet_direction = 1