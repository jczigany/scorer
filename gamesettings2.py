from PySide2.QtWidgets import QMessageBox, QDialog, QDialogButtonBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QRadioButton, QSpinBox, QCompleter
from PySide2.QtCore import *
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
import random

# db = QSqlDatabase.addDatabase('QMYSQL')
# db.setHostName('localhost')
# db.setDatabaseName('cida')
# db.setUserName('cida')
# db.setPassword('cida')

db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('scorer.db3')


class GameSettingsDialog(QDialog):
    def __init__(self, parent = None):
        super(GameSettingsDialog, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setWindowTitle("Game settings")
        # db = db

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.kontener_names = QHBoxLayout()
        self.kontener_buttons = QHBoxLayout()
        self.kontener_szovegek1 = QVBoxLayout()
        self.kontener_sets = QHBoxLayout()
        self.layout.addLayout(self.kontener_names)
        self.layout.addLayout(self.kontener_szovegek1)
        self.layout.addLayout(self.kontener_buttons)
        self.layout.addLayout(self.kontener_sets)

        self.label_player1 = QLabel("Player 1")
        self.input_player1_name = QLineEdit()
        self.input_player1_name.setPlaceholderText("Player 1 name")
        self.input_player1_name.setFocus()
        self.player1_completer = QCompleter()
        self.input_player1_name.setCompleter(self.player1_completer)

        self.label_player2 = QLabel("Player 2")
        self.input_player2_name = QLineEdit()
        self.input_player2_name.setPlaceholderText("Player 2 name")
        self.player2_completer = QCompleter()
        self.input_player2_name.setCompleter(self.player2_completer)

        self.get_player_name()

        self.kontener_names.addWidget(self.label_player1)
        self.kontener_names.addWidget(self.input_player1_name)
        self.kontener_names.addWidget(self.label_player2)
        self.kontener_names.addWidget(self.input_player2_name)

        self.kontener_szovegek1.addWidget(QLabel("Leave Player 2 blank for single player"))
        self.kontener_szovegek1.addWidget(QLabel("Variant"))

        self.gomb_301 = QRadioButton("301")
        self.gomb_401 = QRadioButton("401")
        self.gomb_501 = QRadioButton("501")
        self.gomb_501.setChecked(True)
        self.gomb_701 = QRadioButton("701")

        self.kontener_buttons.addWidget(self.gomb_301)
        self.kontener_buttons.addWidget(self.gomb_401)
        self.kontener_buttons.addWidget(self.gomb_501)
        self.kontener_buttons.addWidget(self.gomb_701)

        self.spin_legs = QSpinBox()
        self.spin_legs.setValue(3)
        self.spin_legs.setMinimum(1)
        self.spin_legs.setMaximum(21)

        self.spin_sets = QSpinBox()
        self.spin_sets.setValue(1)
        self.spin_sets.setMinimum(1)
        self.spin_sets.setMaximum(15)

        self.kontener_sets.addWidget(QLabel("Legs per set: "))
        self.kontener_sets.addWidget(self.spin_legs)
        self.kontener_sets.addWidget(QLabel("Number os sets: "))
        self.kontener_sets.addWidget(self.spin_sets)

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Reset)
        self.buttonbox.clicked.connect(self.buttonbox_click)
        self.layout.addWidget(self.buttonbox)

    def get_player_name(self):
        player_name_model = QSqlQueryModel()
        query = QSqlQuery("SELECT player_name  FROM players order by player_name", db=db)
        player_name_model.setQuery(query)
        self.player1_completer.setModel(player_name_model)
        self.player2_completer.setModel(player_name_model)

    def buttonbox_click(self, b):
        if b.text() == "OK":
            self.accept()
        elif b.text() == "Cancel":
            self.reject()
        else:
            self.alapertekek()

    def alapertekek(self):
        self.input_player1_name.setText("")
        self.input_player1_name.setPlaceholderText("Player 1 name")
        self.input_player2_name.setText("")
        self.input_player2_name.setPlaceholderText("Player 2 name")
        self.gomb_501.setChecked(True)
        self.spin_legs.setValue(3)
        self.spin_sets.setValue(1)

    def accept(self):
        print("OK")

        params = []
        m_id = p1_id = p2_id = set = leg = 0
        var = ""
        player1 = self.input_player1_name.text()
        player2 = self.input_player2_name.text()
        # A MATCH_ID-T AZ AUTOINCREMENTBŐL KELLENE VISSZAKÉRNI ÉS NEM IMPLICIT RANDOMBÓL GENERÁLNI
        m_id = random.randint(10, 1000000)
        # print(m_id)
        set = self.spin_legs.value()
        leg = self.spin_sets.value()
        if self.gomb_301.isChecked():
            var = "301"
        elif self.gomb_401.isChecked():
            var = "401"
        elif self.gomb_501.isChecked():
            var = "501"
        else:
            var = "701"

        player1_id_model = QSqlQueryModel()
        query1 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player1}'", db=db)
        player1_id_model.setQuery(query1)
        if player1_id_model.record(0).value(0):
            p1_id = int(player1_id_model.record(0).value(0))
        else:
            player_model1 = QSqlTableModel()
            player_model1.setTable("players")
            rec_play1 = player_model1.record()
            rec_play1.remove(0)
            rec_play1.setValue(0, player1)
            if player_model1.insertRecord(-1, rec_play1):
                player_model1.submitAll()
            else:
                db.rollback()
            query1 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player1}'", db=db)
            player1_id_model.setQuery(query1)
            p1_id = int(player1_id_model.record(0).value(0))

        player2_id_model = QSqlQueryModel()
        query2 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player2}'", db=db)
        player2_id_model.setQuery(query2)
        if player2_id_model.record(0).value(0):
            p2_id = int(player2_id_model.record(0).value(0))
        else:
            player_model2 = QSqlTableModel()
            player_model2.setTable("players")
            rec_play2 = player_model2.record()
            rec_play2.remove(0)
            rec_play2.setValue(0, player2)
            if player_model2.insertRecord(-1, rec_play2):
                player_model2.submitAll()
            else:
                db.rollback()
            query2 = QSqlQuery(f"SELECT player_id FROM players where player_name = '{player2}'", db=db)
            player2_id_model.setQuery(query2)
            p2_id = int(player2_id_model.record(0).value(0))

        # Match paremeterek rögzítése
        now = QDateTime.currentDateTime()
        match_model = QSqlTableModel()
        match_model.setTable("match_settings")
        record = match_model.record()
        record.setValue(0, m_id)
        record.setValue(1, p1_id)
        record.setValue(2, p2_id)
        record.setValue(3, var)
        record.setValue(4, set)
        record.setValue(5, leg)
        record.setValue(6, now)
        # print(record)
        if match_model.insertRecord(-1, record):
            match_model.submitAll()
        else:
            db.rollback()
        params.append(player1)
        params.append(player2)
        params.append(m_id)
        params.append(p1_id)
        params.append(p2_id)
        params.append(var)
        params.append(set)
        params.append(leg)
        self.parent.new_game_window.params = params
        self.parent.new_game_window.refresh()
        super().accept()


    def reject(self):
        print("CANCEL")
        self.parent.new_game_window.close()
        super().reject()
