"""!
Az új játék beállításainak megadása. Adatbázisból dolgozik (local: sqlite, vagy remote:mysql)
A játékosok neve db-ből (auto completer), ha újat írunk be, azt letárolja
A beállított paramétereket átadja a játéablaknak inicializálásra és bezárja magát.
Ha megszakítjuk, akkor a játékablak is bezáródik
"""
from PySide6.QtWidgets import QMessageBox, QDialog, QDialogButtonBox, QLabel, QLineEdit, QCheckBox, \
    QVBoxLayout, QHBoxLayout, QApplication, QRadioButton, QSpinBox, QCompleter
from PySide6.QtCore import *
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
import random, sys


class GameSettingsDialog(QDialog):
    """!
    Maga a settings-ablak (modal)
    - Alapparaméterek beállítása
    - Adatbázis-kapcsolat létrehozása
    - Widget-ek, Layout-ok létrehozása
    """
    def __init__(self, parent = None):
        super(GameSettingsDialog, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setWindowTitle("Game settings")
        # self.db_connect()

        self.create_widgets()
        self.set_layouts()

    # def db_connect(self):
    #     """
    #     Adatbázis-kapcsolat definiálása, kapcsolat létrehozása
    #     :return:
    #     """
    #     self.db = QSqlDatabase.addDatabase('QMYSQL')
    #     self.db.setHostName('192.168.68.22')
    #     self.db.setDatabaseName('cida')
    #     self.db.setUserName('cida')
    #     self.db.setPassword('cida')
    #     if not self.db.open():
    #         QMessageBox.critical(
    #             None,
    #             "App Name - Error!",
    #             "Database Error: %s" % self.db.lastError().text(),
    #         )
    #         sys.exit(1)

    ## Az ablakon szereplő widget-ek létrehozása
    def create_widgets(self):
        """!
        A játékosnevek completer-el kiegészítve. Az adatokat a get_player_name() tölti be db-ből
        :return:
        """
        self.label_player1 = QLabel("Player 1")
        self.input_player1_name = QLineEdit()
        self.input_player1_name.setPlaceholderText("Player 1")
        self.input_player1_name.setFocus()
        self.player1_completer = QCompleter()
        self.input_player1_name.setCompleter(self.player1_completer)

        self.label_player2 = QLabel("Player 2")
        self.input_player2_name = QLineEdit()
        self.input_player2_name.setPlaceholderText("Player 2")
        self.player2_completer = QCompleter()
        self.input_player2_name.setCompleter(self.player2_completer)
        # player widget-ek feltültése a db-ben szereplő nevekkel, autocomplete-hez
        self.get_player_name()

        self.gomb_301 = QRadioButton("301")
        self.gomb_401 = QRadioButton("401")
        self.gomb_501 = QRadioButton("501")
        self.gomb_501.setChecked(True)
        self.gomb_701 = QRadioButton("701")

        self.label_bestof = QLabel("Best Of.. (Egyébként First To..)")
        self.best_of = QCheckBox()

        self.spin_legs = QSpinBox()
        self.spin_legs.setValue(3)
        self.spin_legs.setMinimum(1)
        self.spin_legs.setMaximum(21)

        self.spin_sets = QSpinBox()
        self.spin_sets.setValue(1)
        self.spin_sets.setMinimum(1)
        self.spin_sets.setMaximum(15)

        self.handi1 = QSpinBox()
        self.handi1.setValue(0)
        self.handi1.setMinimum(-100)
        self.handi1.setMaximum(100)

        self.handi2 = QSpinBox()
        self.handi2.setValue(0)
        self.handi2.setMinimum(-100)
        self.handi2.setMaximum(100)
        ## Az ablak gombjai: OK, Cancel, Reset
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Reset)
        self.buttonbox.clicked.connect(self.buttonbox_click)

    def set_layouts(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.kontener_names = QHBoxLayout()
        self.kontener_names.addWidget(self.label_player1)
        self.kontener_names.addWidget(self.input_player1_name)
        self.kontener_names.addWidget(self.label_player2)
        self.kontener_names.addWidget(self.input_player2_name)

        self.kontener_buttons = QHBoxLayout()
        self.kontener_buttons.addWidget(self.gomb_301)
        self.kontener_buttons.addWidget(self.gomb_401)
        self.kontener_buttons.addWidget(self.gomb_501)
        self.kontener_buttons.addWidget(self.gomb_701)

        self.bestof_layout = QHBoxLayout()
        self.bestof_layout.addWidget(self.label_bestof)
        self.bestof_layout.addWidget(self.best_of)

        self.kontener_szovegek1 = QVBoxLayout()
        self.kontener_szovegek1.addWidget(QLabel("Leave Player 2 blank for single player"))
        self.kontener_szovegek1.addWidget(QLabel("Variant"))

        self.kontener_sets = QHBoxLayout()
        self.kontener_sets.addWidget(QLabel("Legs per set: "))
        self.kontener_sets.addWidget(self.spin_legs)
        self.kontener_sets.addWidget(QLabel("Number os sets: "))
        self.kontener_sets.addWidget(self.spin_sets)

        self.kontener_handi = QHBoxLayout()
        self.kontener_handi.addWidget(QLabel("Handicap (1)"))
        self.kontener_handi.addWidget(self.handi1)
        self.kontener_handi.addWidget(QLabel("Handicap (2)"))
        self.kontener_handi.addWidget(self.handi2)

        self.layout.addLayout(self.kontener_names)
        self.layout.addLayout(self.kontener_szovegek1)
        self.layout.addLayout(self.kontener_buttons)
        self.layout.addLayout(self.bestof_layout)
        self.layout.addLayout(self.kontener_sets)
        self.layout.addLayout(self.kontener_handi)
        self.layout.addWidget(self.buttonbox)

    ## A név completer-ek feltöltése
    def get_player_name(self):
        """!
        A players táblából kiválasztjuk a játékosneveket, akiknek a tipusa 'local' (nem tornát játszunk)
        és a a státuszuk 'aktiv' (nem törölt) és ezt beállítjuk a completer model-jének
        :return:
        """
        player_name_model = QSqlQueryModel()
        query = QSqlQuery("SELECT player_name  FROM players where type='local' and aktiv=1 order by player_name")
        player_name_model.setQuery(query)
        self.player1_completer.setModel(player_name_model)
        self.player2_completer.setModel(player_name_model)

    ## A buttonbox click-jének lekezelése
    def buttonbox_click(self, b):
        """!
        Gomg lenyomások kezelése
        :param b: Melyik gomb lett megnyomva
        :return:
        """
        ## Ha az OK
        if b.text() == "OK":
            ## Akkor lefut az accept
            self.accept()
        ## Ha Cancel
        elif b.text() == "Cancel":
            ## bezárunk mindent
            self.reject()
        ## Reset
        else:
            ## Alapértékek visszaállítása
            self.alapertekek()

    def alapertekek(self):
        self.input_player1_name.setText("")
        self.input_player1_name.setPlaceholderText("Player 1 name")
        self.input_player2_name.setText("")
        self.input_player2_name.setPlaceholderText("Player 2 name")
        self.gomb_501.setChecked(True)
        self.best_of.setChecked(False)
        self.spin_legs.setValue(3)
        self.spin_sets.setValue(1)
        self.handi1.setValue(0)
        self.handi2.setValue(0)

    def accept(self):
        params = []
        m_id = p1_id = p2_id = set = leg = hc1 = hc2 =0
        var = ""
        player1 = self.input_player1_name.text()
        player2 = self.input_player2_name.text()
        # todo A MATCH_ID-T VALAMI EGYEDI MÓDON KELL GENERÁLNI(pl. az időbélyeg bizonyos részével)
        m_id = random.randint(10, 1000000)
        leg = self.spin_legs.value()
        set = self.spin_sets.value()
        hc1 = self.handi1.value()
        hc2 = self.handi2.value()
        if self.gomb_301.isChecked():
            var = "301"
        elif self.gomb_401.isChecked():
            var = "401"
        elif self.gomb_501.isChecked():
            var = "501"
        else:
            var = "701"

        if self.best_of.isChecked():
            bestof = 1
        else:
            bestof = 0

        if len(player1) == 0:
            p1_id = 1
            player1 = "Player 1"
        else:
            player1_id_model = QSqlQueryModel()
            query1 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player1}' and type='local' and aktiv=1")
            player1_id_model.setQuery(query1)
            # todo megnézni, hogy sima query.exec_ -el hogyan működik, lehet-e ellenőrizni, hogy üres vagy nem
            if player1_id_model.record(0).value(0):
                p1_id = int(player1_id_model.record(0).value(0))
            else:
                # todo beszúrás előtt ellenőritni, hogy egyedi-e. Létezhet versenyen felvitt ugyanolyan név
                player_model1 = QSqlTableModel()
                player_model1.setTable("players")
                rec_play1 = player_model1.record()
                rec_play1.remove(0)
                rec_play1.setValue(0, player1)
                rec_play1.setValue(1, 'local')
                rec_play1.setValue(2, 1)
                if player_model1.insertRecord(-1, rec_play1):
                    player_model1.submitAll()
                else:
                    self.parent.db.rollback()
                query1 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player1}' and type='local' and aktiv=1")
                player1_id_model.setQuery(query1)
                # todo megnézni, hogy sima query.exec_ -el hogyan működik, lehet-e ellenőrizni, hogy üres vagy nem
                p1_id = int(player1_id_model.record(0).value(0))

        if len(player2) == 0:
            p2_id = 2
            player2 = "Player 2"
        else:
            player2_id_model = QSqlQueryModel()
            query2 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player2}' and type='local' and aktiv=1")
            player2_id_model.setQuery(query2)
            # todo megnézni, hogy sima query.exec_ -el hogyan működik, lehet-e ellenőrizni, hogy üres vagy nem
            if player2_id_model.record(0).value(0):
                p2_id = int(player2_id_model.record(0).value(0))
            else:
                player_model2 = QSqlTableModel()
                player_model2.setTable("players")
                rec_play2 = player_model2.record()
                rec_play2.remove(0)
                rec_play2.setValue(0, player2)
                rec_play2.setValue(1, 'local')
                rec_play2.setValue(2, 1)
                if player_model2.insertRecord(-1, rec_play2):
                    player_model2.submitAll()
                else:
                    self.parent.db.rollback()
                query2 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player2}' and type='local' and aktiv=1")
                player2_id_model.setQuery(query2)
                # todo megnézni, hogy sima query.exec_ -el hogyan működik, lehet-e ellenőrizni, hogy üres vagy nem
                p2_id = int(player2_id_model.record(0).value(0))

        # Match paremeterek rögzítése
        now = QDateTime.currentDateTime()
        match_model = QSqlTableModel()
        match_model.setTable("match_settings")
        # todo Best Of... nincs db-ben tárolva
        record = match_model.record()
        record.setValue(0, m_id)
        record.setValue(1, p1_id)
        record.setValue(2, p2_id)
        record.setValue(3, var)
        record.setValue(4, leg)
        record.setValue(5, set)
        record.setValue(6, hc1)
        record.setValue(7, hc2)
        record.setValue(8, now)
        if match_model.insertRecord(-1, record):
            match_model.submitAll()
        else:
            self.parent.db.rollback()
        params.append(player1)
        params.append(player2)
        params.append(m_id)
        params.append(p1_id)
        params.append(p2_id)
        params.append(var)
        params.append(leg)
        params.append(set)
        params.append(hc1)
        params.append(hc2)
        params.append(bestof)
        self.parent.new_game_window.params = params
        self.parent.new_game_window.refresh()
        self.parent.db.close()
        super().accept()

    def reject(self):
        self.parent.db.close()
        self.parent.new_game_window.close()
        super().reject()
