class Settings():
    """Klasa przeznaczona do przechowywania wszystkich ustawień gry."""

    def __init__(self):
        """Inicjalizacja ustawień gry."""
        self.screen_width = 1800
        self.screen_height = 900
        self.bg_color = (230, 230, 230)
        #Ustawienia dotyczące statku.
        self.ship_speed = 1.9
        #Ustawienia dotyczące pocisku.
        self.bullet_speed = 1.9
        self.bullet_width = 15
        self.bullet_height = 7
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3