from PySide6.QtGui import QAction

def create_menus(self):
    # Menu
    self.menu = self.menuBar()

    # File menü
    self.file_menu = self.menu.addMenu("File")
    # Exit action
    exit_action = QAction("Kilépés", self)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(self.exit_app)
    self.file_menu.addAction(exit_action)
    # New Game action
    new_game_action = QAction("Új játék", self)
    new_game_action.setShortcut("Ctrl+N")
    new_game_action.triggered.connect(self.new_game)
    self.file_menu.addAction(new_game_action)

    # Tournament menü
    self.tournament_menu = self.menu.addMenu("Torna")
    # Mérkőzés kiválasztása action
    select_torna_action = QAction("Mérkőzés választás", self)
    select_torna_action.triggered.connect(self.select_torna)
    self.tournament_menu.addAction(select_torna_action)

    # Statisztika menü
    self.stat_menu = self.menu.addMenu("Statisztika")
    # Mérkőzés visszanézése
    match_history_action = QAction("Mérkőzés 'visszanézése'", self)
    match_history_action.triggered.connect(self.match_history)
    self.stat_menu.addAction(match_history_action)

    # Beállítások menü
    self.beallitasok_menu = self.menu.addMenu("Beállítások")
    # Paraméterek beállítása action
    beallitasok_action = QAction("Paraméterek beállítása", self)
    beallitasok_action.triggered.connect(self.network_settings)
    self.beallitasok_menu.addAction(beallitasok_action)


def create_menus_org(self):
    # Menu
    self.menu = self.menuBar()

    # File menü
    self.file_menu = self.menu.addMenu("File")
    # Exit action
    exit_action = QAction("Kilépés", self)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(self.exit_app)
    self.file_menu.addAction(exit_action)

    # Tournament menü
    self.tournament_menu = self.menu.addMenu("Torna")
    # Torna szervezése action
    organ_torna_action = QAction("Verseny létrehozása", self)
    organ_torna_action.triggered.connect(self.torna_settings)
    self.tournament_menu.addAction(organ_torna_action)
    # Torna módosítás action
    modify_torna_action = QAction("Verseny módosítása", self)
    modify_torna_action.triggered.connect(self.torna_settings2)
    self.tournament_menu.addAction(modify_torna_action)
    # Torna résztvevők action
    create_tornaplayers_action = QAction("A torna résztvevői", self)
    create_tornaplayers_action.triggered.connect(self.create_players)
    self.tournament_menu.addAction(create_tornaplayers_action)
    # Torna táblák összerakása action
    create_boards_action = QAction("Tornatáblák létrehozása", self)
    create_boards_action.triggered.connect(self.create_boards)
    self.tournament_menu.addAction(create_boards_action)
    # Torna státusza action
    status_torna_action = QAction("Verseny állása", self)
    status_torna_action.triggered.connect(self.torna_status)
    self.tournament_menu.addAction(status_torna_action)