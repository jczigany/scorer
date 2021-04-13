from PySide2.QtWidgets import QAction

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
    # Mérkőzés kiválasztása action
    # select_torna_action = QAction("Mérkőzés választás", self)
    # select_torna_action.triggered.connect(self.select_torna)
    # self.tournament_menu.addAction(select_torna_action)

    # Torna szervezése action
    organ_torna_action = QAction("Verseny létrehozása", self)
    organ_torna_action.triggered.connect(self.torna_settings)
    self.tournament_menu.addAction(organ_torna_action)
