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

    # # Csapat-tagok menü
    # self.member_menu = self.menu.addMenu("Tagság")
    # # Új tag action
    # new_member_action = QAction("Tagok kezelése", self)
    # new_member_action.setShortcut("Ctrl+T")
    # new_member_action.triggered.connect(self.new_member)
    # self.member_menu.addAction(new_member_action)
    #
    # # Befizetések menü
    # self.befizetes_menu = self.menu.addMenu("Bevétel")
    # # Tagdíj befizetés action
    # new_tagdij_action = QAction("Tagdíj befizetés", self)
    # new_tagdij_action.setShortcut("Ctrl+H")
    # new_tagdij_action.triggered.connect(self.new_tagdij)
    # self.befizetes_menu.addAction(new_tagdij_action)
    # # Bérlet vásárlás action
    # new_berlet_action = QAction("Bérlet vásárlás", self)
    # new_berlet_action.setShortcut("Ctrl+B")
    # new_berlet_action.triggered.connect(self.new_berlet)
    # self.befizetes_menu.addAction(new_berlet_action)
    # # Napidíj action
    # new_napidij_action = QAction("Napidíj befizetés", self)
    # new_napidij_action.setShortcut("Ctrl+N")
    # new_napidij_action.triggered.connect(self.new_napidij)
    # self.befizetes_menu.addAction(new_napidij_action)
    # # Adomány action
    # new_adomany_action = QAction("Adomány befizetés", self)
    # new_adomany_action.setShortcut("Ctrl+A")
    # new_adomany_action.triggered.connect(self.new_adomany)
    # self.befizetes_menu.addAction(new_adomany_action)
    # # Egyéb befizetés action
    # new_egyebfiz_action = QAction("Egyéb befizetés", self)
    # new_egyebfiz_action.setShortcut("Ctrl+E")
    # new_egyebfiz_action.triggered.connect(self.new_egyebfiz)
    # self.befizetes_menu.addAction(new_egyebfiz_action)
    #
    # # Kiadások menü
    # self.kiadasok_menu = self.menu.addMenu("Kiadás")
    # # Úk kiadás action
    # new_kifizetes_action = QAction("új kiadás", self)
    # new_kifizetes_action.triggered.connect(self.new_kiadas)
    # self.kiadasok_menu.addAction(new_kifizetes_action)

    # Beállítások menü
    self.beallitasok_menu = self.menu.addMenu("Beállítások")
    # Paraméterek beállítása action
    beallitasok_action = QAction("Paraméterek beállítása", self)
    beallitasok_action.triggered.connect(self.network_settings)
    self.beallitasok_menu.addAction(beallitasok_action)