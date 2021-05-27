from PySide2.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QSpacerItem, QWidget, QMessageBox, QDialog, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication, QSizePolicy, QTextEdit, QInputDialog
from PySide2.QtCore import *
from PySide2.QtGui import QRegExpValidator, QIntValidator, QFont, QTextCursor, QPainter, QPixmap, QPalette, QBrush, QImage
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel


# db = QSqlDatabase.addDatabase('QMYSQL')
# db.setHostName('localhost')
# db.setDatabaseName('cida')
# db.setUserName('cida')
# db.setPassword('cida')
# formátum ******    num1: [ [], [], ....],      ********
kiszallo = {
    170: [['T20', 'T20', 'DB'],],
    167: [['T20', 'T19', 'DB'],],
    164: [['T20', 'T18', 'DB'], ['T19', 'T19', 'DB']],
    161: [['T20', 'T17', 'DB'],],
    160: [['T20', 'T20', 'D20'],],
    158: [['T20', 'T20', 'D19'],],
    157: [['T20', 'T19', 'D20'],],
    156: [['T20', 'T20', 'D18'],],
    155: [['T20', 'T19', 'D19'],],
    154: [['T20', 'T18', 'D20'], ['T19', 'T19', 'D20']],
    153: [['T20', 'T19', "D18"],],
    152: [['T20', 'T20', 'D16'],],
    151: [['T20', 'T17', 'D20'], ['T19', 'T18', 'D20']],
    150: [['T20', 'T18', 'D18'], ['T19', 'T19', 'D18']],
    149: [['T20', 'T19', 'D16'],],
    148: [['T20', 'T20', 'D14'], ['T19', 'T17', 'D20']],
    147: [['T20', 'T17', 'D18'], ['T19', 'T19', 'D18']],
    146: [['T20', 'T18', 'D16'], ['T19', 'T19', 'D16']],
    145: [['T20', 'T19', 'D14'], ['T15', 'T20', 'D20']],
    144: [['T20', 'T20', 'D12'],],
    143: [['T20', 'T17', 'D16'], ['T19', 'T18', 'D16']],
    142: [['T20', 'T14', 'D20'], ['T19', 'T19', 'D14']],
    141: [['T20', 'T19', 'D12'], ['T17', 'T18', 'D18']],
    140: [['T20', 'T20', 'D20'],],
    139: [['T20', 'T13', 'D20'],],
    138: [['T20', 'T18', 'D12'], ['T19', 'T19', 'D12']],
    137: [['T20', 'T19', 'D10'],],
    136: [['T20', 'T20', 'D8'],],
    135: [['DB', 'T15', 'D20'],],
    134: [['T20', 'T16', 'D13'], ['T20', 'T14', 'D16']],
    133: [['T20', 'T19', 'D8'],],
    132: [['DB', 'DB', 'D16'],],
    131: [['T20', 'T13', 'D16'], ['T19', 'T14', 'D16']],
    130: [['T20', 'T20', 'D5'],],
    129: [['T19', 'T16', 'D12'],['T20', 'T19', 'D6']],
    128: [['T18', 'T14', 'D16'], ['T18', 'T18', 'D10']],
    127: [['T20', 'T17', 'D8'],],
    126: [['T19', 'T19', 'D6'],],
    125: [['T18', 'T13', 'D16'], ['T20', 'T15', 'D10']],
    124: [['T20', 'T14', 'D11'],],
    123: [['T19', 'T16', 'D9'],],
    122: [['T18', 'T18', 'D7'],],
    121: [['T20', 'T11', 'D14'], ['T17', 'T20', 'D5']],
    120: [['T20', 'S20', 'D20'],],
    119: [['T19', 'T12', 'D13'],],
    118: [['T20', 'S18', 'D20'],],
    117: [['T20', 'S17', 'D20'], ['T19', 'S20', 'D20']],
    116: [['T19', 'S19', 'D20'], ['T20', 'S16', 'D20']],
    115: [['T19', 'S18', 'D20'], ['T20', 'S15', 'D20']],
    114: [['T20', 'S14', 'D20'], ['T19', 'S17', 'D20']],
    113: [['T19', 'S16', 'D20'],],
    112: [['T20', 'T12', 'D8'],],
    111: [['T20', 'S11', 'D20'], ['T19', 'S14', 'D20']],
    110: [['T20', 'T10', 'D10'], ['T19', 'S13', 'D20'], ['T20', 'DB']],
    109: [['T20', 'S9', 'D20'], ['T19', 'T12', 'D8']],
    108: [['T20', 'S16', 'D16'], ['T19', 'S11', 'D20']],
    107: [['T19', 'T10', 'D10'], ['T19', 'DB']],
    106: [['T20', 'T10', 'D8'],],
    105: [['T20', 'S13', 'D16'],],
    104: [['T19', 'S15', 'D16'], ['T18', 'DB']],
    103: [['T19', 'S10', 'D18'], ['T19', 'S6', 'D20']],
    102: [['T20', 'S10', 'D16'],],
    101: [['T20', 'S9', 'D16'], ['T19', 'T12', 'D4'], ['T17', 'DB']],
    100: [['T20', 'D20'],],
    99: [['T19', 'S10', 'D16'],],
    98: [['T20', 'D19'],],
    97: [['T19', 'D20'],],
    96: [['T20', 'D18'],],
    95: [['SB', 'T20', 'D5'], ['T19', 'D19']],
    94: [['SB', 'T19', 'D6'], ['T18', 'D20']],
    93: [['SB', 'T18', 'D7'], ['T19', 'D18']],
    92: [['T20', 'D16'], ['SB', 'T17', 'D8']],
    91: [['T17', 'D20'], ['SB', 'T16', 'D9']],
    90: [['T18', 'D18'], ['T20', 'D15']],
    89: [['T19', 'D16'],],
    88: [['T20', 'D14'],],
    87: [['T17', 'D18'],],
    86: [['T18', 'D16'],],
    85: [['T19', 'D14'], ['T15', 'D20']],
    84: [['T20', 'D12'],],
    83: [['T17', 'D16'],],
    82: [['T14', 'D20'], ['DB', 'D16']],
    81: [['T19', 'D12'], ['T15', 'D18']],
    80: [['T20', 'D10'],],
    79: [['T19', 'D11'], ['T13', 'D20']],
    78: [['T18', 'D12'],],
    77: [['T19', 'D10'],],
    76: [['T20', 'D8'], ['T16', 'D14']],
    75: [['T17', 'D12'],],
    74: [['T14', 'D16'],],
    73: [['T19', 'D8'],],
    72: [['T16', 'D12'], ['T20', 'D6']],
    71: [['T13', 'D16'], ['T17', 'D10'], ['T19', 'D7']],
    70: [['T18', 'D8'], ['T20', 'D5']],
    69: [['T19', 'D6'],],
    68: [['T16', 'D10'], ['T20', 'D4'], ['T18', 'D7']],
    67: [['T17', 'D8'], ['T9', 'D20']],
    66: [['T10', 'D18'], ['T18', 'D6'], ['T16', 'D9']],
    65: [['T19', 'D4'], ['T15', 'D10'], ['T11', 'D16']],
    64: [['T16', 'D8'], ['T14', 'D11']],
    63: [['T17', 'D6'], ['T13', 'D12']],
    62: [['T10', 'D16'], ['T12', 'D13']],
    61: [['T15', 'D8'], ['T11', 'D14']],
    60: [['S20', 'D20'],],
    59: [['S19', 'D20'],],
    58: [['S18', 'D20'],],
    57: [['S17', 'D20'],],
    56: [['T16', 'D4'],],
    55: [['S15', 'D20'],],
    54: [['S14', 'D20'],],
    53: [['S13', 'D20'], ['S17', 'D18']],
    52: [['T12', 'D8'],],
    51: [['S11', 'D20'], ['S15', 'D18']],
    50: [['S10', 'D20'],],
    49: [['S9', 'D20'],],
    48: [['S16', 'D16'],],
    47: [['S15', 'D16'], ['S7', 'D20']],
    46: [['S6', 'D20'], ['S10', 'D18']],
    45: [['S13', 'D16'],],
    44: [['S12', 'D16'], ['S4', 'D20']],
    43: [['S11', 'D16'], ['S3', 'D20']],
    42: [['S10', 'D16'], ['S6', 'D18']],
    41: [['S9', 'D16'],],
    40: [['D20'],],
    39: [['S7', 'D16'], ['S19', 'D10'], ['S3', 'D18']],
    38: [['D19'], ['S6', 'D16'], ['S10', 'D14']],
    37: [['S5', 'D16'],],
    36: [['D18'],],
    35: [['S2', 'D16'],],
    34: [['D17'], ['S6', 'D14'], ['S10', 'D12'] ],
    33: [['S1', 'D16'], ['S17', 'D8']],
    32: [['D16'],],
    31: [['S15', 'D8'],],
    30: [['D15'], ['S10', 'D10']],
    29: [['S13', 'D8'],],
    28: [['D14'],],
    27: [['S19', 'D4'], ['S7', 'D10'], ['S11', 'D8']],
    26: [['D13'],],
    25: [['S17', 'D4'], ['S9', 'D8']],
    24: [['D12'],],
    23: [['S7', 'D8'],],
    22: [['D11'],],
    21: [['S5', 'D8'], ['S17', 'D2']],
    20: [['D10'],],
    19: [['S11', 'D4'], ['S3', 'D8']],
    18: [['D9'],],
    17: [['S9', 'D4'], ['S1', 'D8']],
    16: [['D8'],],
    15: [['S7', 'D4'],],
    14: [['D7'], ['S6', 'D4'], ['S10', 'D2']],
    13: [['S5', 'D4'],],
    12: [['D6'],],
    11: [['S3', 'D4'],],
    10: [['D5'],],
    9: [['S1', 'D4'],],
    8: [['D4'],],
    7: [['S3', 'D2'],],
    6: [['D3'], ['S2', 'D2']],
    5: [['S1', 'D2'],],
    4: [['D2'],],
    3: [['S1', 'D1'],],
    2: [['D1'],],
}

# db = QSqlDatabase.addDatabase('QSQLITE')
# db.setDatabaseName('scorer.db3')
#
# if not db.open():
#     QMessageBox.critical(
#         None,
#         "App Name - Error!",
#         "Database Error: %s" % db.lastError().text(),
#     )
#     sys.exit(1)

class CustomQLineEdit(QLineEdit):
    def __init__(self, parent):
        super(CustomQLineEdit, self).__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.setText("0")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F2:
            self.setText("26")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F3:
            self.setText("41")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F4:
            self.setText("45")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F5:
            self.setText("60")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F6:
            self.setText("81")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F7:
            self.setText("85")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F8:
            self.setText("100")
            self.returnPressed.emit()
        elif event.key() == Qt.Key_F9:
            if self.parent.akt_score == 'score_1':
                self.setText(str(int(self.parent.pont1.text()) - int(self.text())))
            else:
                self.setText(str(int(self.parent.pont2.text()) - int(self.text())))
            self.returnPressed.emit()
        elif event.key() == Qt.Key_Right:
            self.change_starter()
            # self.returnPressed.emit()
        elif event.key()  == Qt.Key_Escape:
            pass
        elif (event.modifiers() & Qt.ControlModifier) and event.key() == Qt.Key_B:
            self.visszavon()
        else:
            QLineEdit.keyPressEvent(self, event)

    def visszavon(self):
        # 1.a a dobas táblából az utolsó rekordot kiolvasni, \
        # dobás értékét + round_number-t, player_id-t megállapítani (match_id, set_id, leg_id, last)
        query = QSqlQuery(f"select * from dobas where match_id={self.parent.match_id} order by timestamp desc limit 1")
        rec_model = QSqlQueryModel()
        rec_model.setQuery(query)
        score = int(rec_model.record(0).value(2))
        kor = int(rec_model.record(0).value(1))
        jatekos = int(rec_model.record(0).value(0))
        if self.parent.akt_score == 'score_1':
            if int(self.parent.pont2.text()) != (int(self.parent.variant) + int(self.parent.params[9])):
                self.parent.akt_score = 'score_2'
                # 3.a az adott játékos pontszámát megnövelni a dobott ponttal (pont1, pont2)
                self.parent.pont2.setText(str(int(self.parent.pont2.text()) + score))
                # 3.b dobások listájából kivenni az utolsót
                cursor = self.parent.kor2.textCursor()
                cursor.movePosition(QTextCursor.End)
                cursor.select(QTextCursor.LineUnderCursor)
                cursor.removeSelectedText()
                cursor.deletePreviousChar()
                self.parent.kor2.setTextCursor(cursor)
                # csak ha a 2. játékosnál vonunk vissza
                self.parent.round_number -= 1
                # 4. a kovetkezo_jatekos-bol "kivenni" a játékos váltást
                self.parent.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                self.parent.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                # 5. dobas táblából törölni a kiválasztott rekordot
                query1 = QSqlQuery(f"delete from dobas where match_id = {self.parent.match_id} and set_id = {self.parent.set_id} and leg_id = {self.parent.leg_id} and round_number = {kor} and player_id = {jatekos}", db=db)
                query1.exec_()
            else:
                pass
        else:
            if int(self.parent.pont1.text()) != (int(self.parent.variant) + int(self.parent.params[8])):
                self.parent.akt_score = 'score_1'
                # 3.a az adott játékos pontszámát megnövelni a dobott ponttal (pont1, pont2)
                self.parent.pont1.setText(str(int(self.parent.pont1.text()) + score))
                # 3.b dobások listájából kivenni az utolsót
                cursor = self.parent.kor1.textCursor()
                cursor.movePosition(QTextCursor.End)
                cursor.select(QTextCursor.LineUnderCursor)
                cursor.removeSelectedText()
                cursor.deletePreviousChar()
                self.parent.kor1.setTextCursor(cursor)
                # csak ha a 2. játékosnál vonunk vissza
                # self.parent.round_number -= 1
                # 4. a kovetkezo_jatekos-bol "kivenni" a játékos váltást
                self.parent.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                self.parent.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                # 5. dobas táblából törölni a kiválasztott rekordot
                query1 = QSqlQuery(
                    f"delete from dobas where match_id = {self.parent.match_id} and set_id = {self.parent.set_id} and leg_id = {self.parent.leg_id} and round_number = {kor} and player_id = {jatekos}",db=db)
                query1.exec_()
            else:
                pass

    def change_starter(self):
        if (int(self.parent.pont1.text()) ==  int(self.parent.params[5]) + self.parent.params[8]) and (int(self.parent.pont2.text()) ==  int(self.parent.params[5]) + self.parent.params[9]) and (self.parent.leg_id == 1) and (self.parent.set_id == 1):
            if self.parent.akt_score == 'score_1':
                self.parent.akt_score = 'score_2'
                self.parent.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                self.parent.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                self.parent.leg_kezd = "player2"
                self.parent.set_kezd = "player2"
            else:
                self.parent.akt_score = 'score_1'
                self.parent.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                self.parent.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                self.parent.leg_kezd = "player1"
                self.parent.set_kezd = "player1"


class CustomQLabel(QLabel):
    def __init__(self, param = ""):
        super(CustomQLabel, self).__init__()
        self.setText(param)
        self.setTextFormat(Qt.RichText)
        self.setStyleSheet("font-size: 22px; font-family: Cuorier New")
        self.setAlignment(Qt.AlignCenter)


class CustomHelpLabel(QLabel):
    def __init__(self, param = ""):
        super(CustomHelpLabel, self).__init__()
        self.setText(param)
        self.setFixedWidth(70)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: lightgray; font-size: 18px")


class CustomIntLabel(CustomQLabel):
    def __init__(self):
        super(CustomIntLabel, self).__init__()
        self.ertek = 0
        self.setText(str(self.ertek))

    def get_value(self):
        return int(self.text())

    def set_value(self, ertek):
        self.ertek = ertek
        self.setText(str(self.ertek))


class CustomFloatLabel(CustomQLabel):
    def __init__(self):
        super(CustomFloatLabel, self).__init__()
        self.ertek = 0.00
        self.setText(str(self.ertek))

    def get_value(self):
        return round(float(self.text()), 2)

    def set_value(self, ertek):
        self.ertek = round(ertek, 2)
        self.setText(str(self.ertek))


class GameWindowDialog(QDialog):
    def __init__(self, parent, place="local"):
        super(GameWindowDialog, self).__init__(parent)
        self.parent = parent
        self.place = place
        self.setModal(True)
        self.showMaximized()

        self.params = []
        self.background_image = QImage("images/gdc_logo_uj.png")
        self.image_rect = QRect()

        self.set_layouts()
        self.alapertekek()
        self.help_felirat()
        # A neveket tartalmazó QLabel-ek létrehozása, hozzáadása a neveket tartalmazó layout-hoz
        self.nev_widgetek()
        # A konkrét pontszámot tartalmazó widget hozzáadása a pont1 widget layout-jához
        self.pontszamok()
        # A CHEKOUT1-ET tartalmazó Widget hozzáadása a checkout1 widget layout-jához
        self.checkouts()
        # Az aktuális pontszámot tartalmazó Widget hozzáadása a current widget layout-jához
        self.dobott_pontszam()
        # A statisztika1-et tartalmazo widget hozzáadása a stat1 layout-hoz
        self.player1_stat()
        # A statisztika2-et tartalmazo widget hozzáadása a stat2 layout-hoz
        self.player2_stat()
        # A körök1(2)-et tartalmazo widget hozzáadása a korok1(2) layout-hoz
        self.dobasok_listaja()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawWidget(painter)
        painter.end()

    def drawWidget(self, painter):
        rect = self.rect()
        hatter = self.background_image.scaled(QSize(rect.width(), rect.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_rect.setRect(rect.x(), rect.y(), hatter.width(), hatter.height())
        self.image_rect.moveCenter(rect.center())
        painter.setOpacity(0.05)
        painter.drawImage(self.image_rect, QImage(hatter))

    def dobott_pontszam(self):
        # Az aktuális pontszámot tartalmazó Widget hozzáadása a current widget layout-jához
        validator = QIntValidator(0, 180)
        self.current = CustomQLineEdit(self)
        self.current.setValidator(validator)
        self.current.setFocus()
        self.current.setAlignment(Qt.AlignCenter)
        self.current.setStyleSheet("border-radius: 5px; font-size: 100px;")
        self.current_layout.addWidget(self.current)
        self.current.returnPressed.connect(self.pont_beirva)

    def pontszamok(self):
        self.pont1 = QLabel("501")
        self.pont1.setAlignment(Qt.AlignCenter)
        self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
        self.score1_layout.addWidget(self.pont1)
        # Set, Leg megjelenítéséhez Widget, Layout
        self.eredmeny_widgetek()
        # # A konkrét pontszámot tartalmazó widget hozzáadása a pont2 widget layout-jához
        self.pont2 = QLabel("501")
        self.pont2.setAlignment(Qt.AlignCenter)
        self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
        self.score2_layout.addWidget(self.pont2)

    def checkouts(self):
        # A CHEKOUT1-ET tartalmazó Widget hozzáadása a checkout1 widget layout-jához
        self.check1 = QTextEdit()
        self.check1.setDisabled(True)
        self.check1.setAlignment(Qt.AlignLeft)
        self.check1.setWindowFlag(Qt.FramelessWindowHint)
        self.check1.setAttribute(Qt.WA_TranslucentBackground)
        self.check1.setStyleSheet("background:transparent;font-size: 33px; color: red")

        cimke1 = QLabel("Kiszálló javaslat:")
        cimke1.setStyleSheet("font-size: 20px")
        cimke2 = QLabel("Kiszálló javaslat:")
        cimke2.setStyleSheet("font-size: 20px")
        self.check1_layout.addWidget(cimke1)
        self.check1_layout.addWidget(self.check1)
        # A CHEKOUT2-ET tartalmazó Widget hozzáadása a checkout2 widget layout-jához
        self.check2 = QTextEdit()
        self.check2.setDisabled(True)
        self.check2.setAlignment(Qt.AlignRight)
        # self.check2.setStyleSheet("font-size: 20px; color: red")
        self.check2.setWindowFlag(Qt.FramelessWindowHint)
        self.check2.setAttribute(Qt.WA_TranslucentBackground)
        self.check2.setStyleSheet("background:transparent;font-size: 33px; color: red")
        self.check2_layout.addWidget(cimke2)
        self.check2_layout.addWidget(self.check2)

    def dobasok_listaja(self):
        # A körök1-et tartalmazo widget hozzáadása a korok1 layout-hoz
        self.kor1 = QTextEdit()
        self.kor1.setAlignment(Qt.AlignCenter)
        self.kor1.setWindowFlag(Qt.FramelessWindowHint)
        self.kor1.setAttribute(Qt.WA_TranslucentBackground)
        self.kor1.setStyleSheet("background:transparent;border-radius: 5px; font-size: 22px")
        self.round1_layout.addWidget(self.kor1)
        # A körök2-et tartalmazo widget hozzáadása a korok2 layout-hoz
        self.kor2 = QTextEdit()
        self.kor2.setAlignment(Qt.AlignCenter)
        self.kor2.setWindowFlag(Qt.FramelessWindowHint)
        self.kor2.setAttribute(Qt.WA_TranslucentBackground)
        self.kor2.setStyleSheet("background:transparent;border-radius: 5px; font-size: 22px")
        self.round2_layout.addWidget(self.kor2)

    def eredmeny_widgetek(self):
        # Set1, Leg1 megjelenítéséhez Widget, Layout
        self.leg1 = QLabel("0")
        self.leg1.setFixedWidth(200)
        self.leg1.setAlignment(Qt.AlignRight)
        self.leg1.setStyleSheet("font-size: 35px; font-weight: bold")
        self.leg1_layout.addWidget(self.leg1)
        self.set1 = QLabel("0")
        self.set1.setFixedWidth(200)
        self.set1.setAlignment(Qt.AlignRight)
        self.set1.setStyleSheet("font-size: 35px; font-weight: bold")
        self.set1_layout.addWidget(self.set1)

        # A Leg és szet felirat külön
        self.leg_cimke = QLabel("Legs")
        self.leg_cimke.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.leg_cimke.setStyleSheet("font-size: 33px")
        self.set_cimke = QLabel("Sets")
        self.set_cimke.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.set_cimke.setStyleSheet("font-size: 33px")
        self.legset_layout.addWidget(self.leg_cimke)
        self.legset_layout.addWidget(self.set_cimke)

        # Set2, Leg2 megjelenítéséhez Widget, Layout
        self.leg2 = QLabel("0")
        self.leg2.setFixedWidth(200)
        self.leg2.setAlignment(Qt.AlignLeft)
        self.leg2.setStyleSheet("font-size: 35px; font-weight: bold")
        self.leg2_layout.addWidget(self.leg2)
        self.set2 = QLabel("0")
        self.set2.setFixedWidth(200)
        self.set2.setAlignment(Qt.AlignLeft)
        self.set2.setStyleSheet("font-size: 35px; font-weight: bold")
        self.set2_layout.addWidget(self.set2)

    def nev_widgetek(self):
        # A neveket tartalmazó QLabel-ek létrehozása, hozzáadása a neveket tartalmazó layout-hoz
        self.nev1 = QLabel()
        self.nev1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.nev1.setStyleSheet("border-radius: 5px; font-size: 50px; font-family: Cuorier New; font-weight: bold")
        self.nev2 = QLabel()
        self.nev2.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.nev2.setStyleSheet("border-radius: 5px; font-size: 50px; font-family: Cuorier New; font-weight: bold")
        self.nevek_layout.addWidget(self.nev1)
        self.nevek_layout.addWidget(self.nev2)

    def check_kiszallo(self, jatekos, pont):
        p = int(pont)
        kisz = []
        if p in  kiszallo:
            kisz = kiszallo[p]
            hossz = len(kisz)   # hány fajta kiszálló van (1-3)
            if jatekos == self.player1_id:  # Az 1-es játékos esetén
                self.check1.clear()         # Töröljük a kiszálló mezőt
                if hossz == 1:              # Ha csak 1 fajta kiszálló van
                    k_string = str(kisz[0][0])
                    for x in range(1,len(kisz[0])):
                        k_string += (" - " + str(kisz[0][x]))
                    self.check1.append(k_string)
                else:
                    for i in range(hossz):
                        k_string = str(kisz[i][0])
                        for x in range(1, len(kisz[i])):
                            k_string += (" - " + str(kisz[i][x]))
                        self.check1.append(k_string)
            else:
                self.check2.clear()
                if hossz == 1:              # Ha csak 1 fajta kiszálló van
                    k_string = str(kisz[0][0])
                    for x in range(1,len(kisz[0])):
                        k_string += (" - " + str(kisz[0][x]))
                    self.check2.append(k_string)
                else:
                    for i in range(hossz):
                        k_string = str(kisz[i][0])
                        for x in range(1, len(kisz[i])):
                            k_string += (" - " + str(kisz[i][x]))
                        self.check2.append(k_string)
        else:
            if jatekos == self.player1_id:
                self.check1.clear()
            else:
                self.check2.clear()

    def player1_stat(self):
        stat1_grid = QGridLayout()
        self.stat1_layout.addLayout(stat1_grid)
        space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.stat1_layout.addItem(space)

        stat1_grid.addWidget(CustomQLabel("60+"), 0, 0)
        self.var60_1 = CustomIntLabel()
        stat1_grid.addWidget(self.var60_1, 0, 1)
        stat1_grid.addWidget(CustomQLabel("80+"), 1, 0)
        self.var80_1 = CustomIntLabel()
        stat1_grid.addWidget(self.var80_1, 1, 1)
        stat1_grid.addWidget(CustomQLabel("100+"), 2, 0)
        self.var100_1 = CustomIntLabel()
        stat1_grid.addWidget(self.var100_1, 2, 1)
        stat1_grid.addWidget(CustomQLabel("120+"), 3, 0)
        self.var120_1 = CustomIntLabel()
        stat1_grid.addWidget(self.var120_1, 3, 1)
        stat1_grid.addWidget(CustomQLabel("140+"), 4, 0)
        self.var140_1 = CustomIntLabel()
        stat1_grid.addWidget(self.var140_1, 4, 1)
        stat1_grid.addWidget(CustomQLabel("180"), 5, 0)
        self.var180_1 = CustomIntLabel()
        stat1_grid.addWidget(self.var180_1, 5, 1)
        stat1_grid.addWidget(QLabel(), 6, 0)

        stat1_grid.addWidget(CustomQLabel("Max kiszálló"), 7, 0)
        self.maxchceck_1 = CustomIntLabel()
        stat1_grid.addWidget(self.maxchceck_1, 7, 1)
        stat1_grid.addWidget(CustomQLabel("Legjobb leg"), 8, 0)
        self.bestleg_1 = CustomIntLabel()
        stat1_grid.addWidget(self.bestleg_1, 8, 1)

        stat1_grid.addWidget(QLabel(), 9, 0)
        stat1_grid.addWidget(CustomQLabel("Dobás átlag"), 10, 0)
        self.aver_1 = CustomFloatLabel()
        stat1_grid.addWidget(self.aver_1, 10, 1)
        stat1_grid.addWidget(CustomQLabel("Első 9 nyíl"), 11, 0)
        self.first9_1 = CustomFloatLabel()
        stat1_grid.addWidget(self.first9_1, 11, 1)

    def player2_stat(self):
        stat2_grid = QGridLayout()
        self.stat2_layout.addLayout(stat2_grid)
        space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.stat2_layout.addItem(space)

        stat2_grid.addWidget(CustomQLabel("60+"), 0, 0)
        self.var60_2 = CustomIntLabel()
        stat2_grid.addWidget(self.var60_2, 0, 1)
        stat2_grid.addWidget(CustomQLabel("80+"), 1, 0)
        self.var80_2 = CustomIntLabel()
        stat2_grid.addWidget(self.var80_2, 1, 1)
        stat2_grid.addWidget(CustomQLabel("100+"), 2, 0)
        self.var100_2 = CustomIntLabel()
        stat2_grid.addWidget(self.var100_2, 2, 1)
        stat2_grid.addWidget(CustomQLabel("120+"), 3, 0)
        self.var120_2 = CustomIntLabel()
        stat2_grid.addWidget(self.var120_2, 3, 1)
        stat2_grid.addWidget(CustomQLabel("140+"), 4, 0)
        self.var140_2 = CustomIntLabel()
        stat2_grid.addWidget(self.var140_2, 4, 1)
        stat2_grid.addWidget(CustomQLabel("180"), 5, 0)
        self.var180_2 = CustomIntLabel()
        stat2_grid.addWidget(self.var180_2, 5, 1)
        stat2_grid.addWidget(QLabel(), 6, 0)

        stat2_grid.addWidget(CustomQLabel("Max kiszálló"), 7, 0)
        self.maxchceck_2 = CustomIntLabel()
        stat2_grid.addWidget(self.maxchceck_2, 7, 1)
        stat2_grid.addWidget(CustomQLabel("Legjobb leg"), 8, 0)
        self.bestleg_2 = CustomIntLabel()
        stat2_grid.addWidget(self.bestleg_2, 8, 1)

        stat2_grid.addWidget(QLabel(), 9, 0)
        stat2_grid.addWidget(CustomQLabel("Dobás átlag"), 10, 0)
        self.aver_2 = CustomFloatLabel()
        stat2_grid.addWidget(self.aver_2, 10, 1)
        stat2_grid.addWidget(CustomQLabel("Első 9 nyíl"), 11, 0)
        self.first9_2 = CustomFloatLabel()
        stat2_grid.addWidget(self.first9_2, 11, 1)

    def update_best_leg_checkout(self, player, pont, nyil):
        if player == self.player1_id:
            if pont > self.maxchceck_1.get_value():
                self.maxchceck_1.set_value(pont)
            if ((self.round_number * 3) - 3 + nyil) < self.bestleg_1.get_value() or self.bestleg_1.get_value() == 0:
                self.bestleg_1.set_value((self.round_number * 3) - 3 + nyil)
        else:
            if pont > self.maxchceck_2.get_value():
                self.maxchceck_2.set_value(pont)
            if ((self.round_number * 3) - 3 + nyil) < self.bestleg_2.get_value() or self.bestleg_2.get_value() == 0:
                self.bestleg_2.set_value((self.round_number * 3) - 3 + nyil)

    def update_score_avg(self, player, pont, nyil):
        if player == self.player1_id:
            if pont == 180:
                self.var180_1.set_value(self.var180_1.get_value() + 1)
            elif pont >= 140:
                self.var140_1.set_value(self.var140_1.get_value() + 1)
            elif pont >= 120:
                self.var120_1.set_value(self.var120_1.get_value() + 1)
            elif pont >= 100:
                self.var100_1.set_value(self.var100_1.get_value() + 1)
            elif pont >= 80:
                self.var80_1.set_value(self.var80_1.get_value() + 1)
            elif pont >= 60:
                self.var60_1.set_value(self.var60_1.get_value() + 1)
            # Átlag számítás
            self.sum_1 += pont
            self.darab_1 += nyil
            self.aver_1.set_value((self.sum_1 / self.darab_1) * 3)
            # 9 nyilas átlag (self.sum9_1, self.darab9_1)
            if self.round_number <= 3:
                self.sum9_1 += pont
                self.darab9_1 += nyil
                self.first9_1.set_value((self.sum9_1 / self.darab9_1) * 3)
        else:
            # print("2. játékos stat")
            if pont == 180:
                self.var180_2.set_value(self.var180_2.get_value() + 1)
            elif pont >= 140:
                self.var140_2.set_value(self.var140_2.get_value() + 1)
            elif pont >= 120:
                self.var120_2.set_value(self.var120_2.get_value() + 1)
            elif pont >= 100:
                self.var100_2.set_value(self.var100_2.get_value() + 1)
            elif pont >= 80:
                self.var80_2.set_value(self.var80_2.get_value() + 1)
            elif pont >= 60:
                self.var60_2.set_value(self.var60_2.get_value() + 1)
            # Átlag számítás
            self.sum_2 += pont
            self.darab_2 += nyil
            self.aver_2.set_value((self.sum_2 / self.darab_2) * 3)
            # 9 nyilas átlag (self.sum9_2, self.darab9_2)
            if self.round_number <= 3:
                self.sum9_2 += pont
                self.darab9_2 += nyil
                self.first9_2.set_value((self.sum9_2 / self.darab9_2) * 3)

    def dobas(self, player, score, nyil=3):
        """
        Az aktuális,érvényes dobás beszúrása a dobas táblába.
        [player_id(player), round_number, points(score), leg_id, set_id, match_id, timestamp]
        :param player:
        :param score:
        :return:
        """
        now = QDateTime.currentDateTime()
        dobas_model = QSqlTableModel()
        dobas_model.setTable("dobas")
        record = dobas_model.record()
        record.setValue(0, player)
        record.setValue(1, (self.round_number * 3) -3 + nyil)
        record.setValue(2, score)
        record.setValue(3, self.leg_id)
        record.setValue(4, self.set_id)
        record.setValue(5, self.match_id)
        record.setValue(6, now)
        if dobas_model.insertRecord(-1, record):
            dobas_model.submitAll()
        else:
            db.rollback()

    def write_leg(self, winner):
        """
        Az aktuális(megnyert) leg beszúrása a matches táblába.
        [match_id, leg_id, set_id, winner_id, timestamp]
        :param winner:
        :return:
        """
        now = QDateTime.currentDateTime()
        leg_model = QSqlTableModel()
        leg_model.setTable("matches")
        record = leg_model.record()
        record.setValue(0, self.match_id)
        record.setValue(1, self.leg_id)
        record.setValue(2, self.set_id)
        record.setValue(3, winner)
        record.setValue(4, now)
        if leg_model.insertRecord(-1, record):
            leg_model.submitAll()
        else:
            db.rollback()
        # todo: nem befejettek esetén előzmények törlése????

    def kovetkezo_jatekos(self, write_score, nyil=3):
        if self.akt_score == 'score_1':
            self.dobas(self.player1_id, write_score, nyil)
            self.kor1.append(str((3 * self.round_number) -3 + nyil) + ":\t" + str(write_score) + "\t" + self.pont1.text())
            self.akt_score = 'score_2'
            self.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
            self.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
        else:
            self.dobas(self.player2_id, write_score, nyil)
            self.kor2.append(str((3 * self.round_number) -3 + nyil) + ":\t" + str(write_score) + "\t" + self.pont2.text())
            self.akt_score = 'score_1'
            self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
            self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")

    def end_game(self):
        self.current.setDisabled(True)
        self.kor1.setDisabled(True)
        self.kor2.setDisabled(True)
        self.check1.clear()
        self.check2.clear()
        if self.place == "network":
            query = QSqlQuery(f"update torna_match set match_status=2 where match_id={self.match_id}")
            query.exec_()

    def result_status(self):
        """
                self.setperleg: Hány Leg-et kell nyerni 1 Set-hez
                self.sets: Hány Set-et kell nyerni a meccs-hez
                self.leg_id: Hányadik Leg az adott Set-ben
                self.set_id: Hányadik Set az adott meccs-ben
        """
        # db1: az adott mecs, adott set-jében hány leg-et nyert az 1. játékos
        # db2: az adott mecs, adott set-jében hány leg-et nyert az 2. játékos
        db1_model = QSqlQueryModel()
        query = QSqlQuery(f"SELECT count(*) db FROM matches where match_id = {self.match_id} and set_id = {self.set_id} and winner_id = {self.player1_id}")
        db1_model.setQuery(query)
        if db1_model.record(0).value(0):
            db1 = int(db1_model.record(0).value(0))
        else:
            db1 = 0
        db2_model = QSqlQueryModel()
        query2 = QSqlQuery(
            f"SELECT count(*) db FROM matches where match_id = {self.match_id} and set_id = {self.set_id} and winner_id = {self.player2_id}")
        db2_model.setQuery(query2)
        if db2_model.record(0).value(0):
            db2 = int(db2_model.record(0).value(0))
        else:
            db2 = 0
        # Elleőrizzük, hogy best vagy first (Ha Set-re játszuk, akkor nem lehet best, csak first
        if not self.bestof:
            # mindketten kevesebbet nyertek, mint kellene
            if (self.legsperset > db1) and (self.legsperset > db2):
                # Az adott set-ben megnöveljük a leg_id-t
                self.leg_id += 1
            else:
                # Ha valamelyik megnyerte a set-et, akkor növeljük a nyert set-ek számát
                if self.legsperset == db1:
                    self.won_sets_1 += 1
                    self.set1.setText(str(self.won_sets_1))
                else:
                    self.won_sets_2 += 1
                    self.set2.setText(str(self.won_sets_2))
                # Ha valaki megnyerte a Set-et, de a meccsnek még nincs vége

                if (self.sets > self.won_sets_1) and ( self.sets > self.won_sets_2):
                    # Átállítjuk, hogy ki kezdte/kezdi a set-et
                    if self.set_kezd == 'player1':
                        self.set_kezd = 'player2'
                        self.leg_kezd = 'player1'
                    else:
                        self.set_kezd = 'player1'
                        self.leg_kezd = 'player2'
                    self.set_id += 1
                    self.leg_id = 1

                    # Leg-számok nullázása
                    self.won_legs_1 = 0
                    self.won_legs_2 = 0
                    self.leg1.setText(str(self.won_legs_1))
                    self.leg2.setText(str(self.won_legs_2))
                else:
                    msg = QMessageBox()
                    msg.setStyleSheet("fonz-size: 20px")
                    msg.setWindowTitle("A játék véget ért!")
                    # Vége a meccsnek, valaki nyert
                    if self.won_sets_1 > self.won_sets_2:
                        msg.setText('<html style="font-size: 16px;">A játékot nyerte:  </html>' + '<html style="font-size: 20px; color: red">' + self.nev1.text() + '</html')
                    else:
                        msg.setText('<html style="font-size: 16px;">A játékot nyerte:  </html>' + '<html style="font-size: 20px; color: red">' + self.nev2.text() + '</html')
                    msg.exec_()
                    self.end_game()
        else:
            # mindketten kevesebbet nyertek, mint kellene
            if (self.legsperset >= (2 * db1)) and (self.legsperset >= (2 * db2)) and (self.legsperset > (db1 + db2)):
                self.leg_id += 1
            else:
                # Mivel nem SET-re játszunk, csak azt kell nézni, hogy mi az eredmény és vége
                msg = QMessageBox()
                msg.setStyleSheet("fonz-size: 20px")
                msg.setWindowTitle("A játék véget ért!")
                if db1 == db2:
                    msg.setText(
                        '<html style="font-size: 16px;">A játékeredménye:  </html>' + '<html style="font-size: 20px; color: red">' + "DÖNTETLEN" + '</html')
                else:
                    if db1 > db2:
                        msg.setText(
                            '<html style="font-size: 16px;">A játékot nyerte:  </html>' + '<html style="font-size: 20px; color: red">' + self.nev1.text() + '</html')
                    else:
                        msg.setText(
                            '<html style="font-size: 16px;">A játékot nyerte:  </html>' + '<html style="font-size: 20px; color: red">' + self.nev2.text() + '</html')
                msg.exec_()
                self.end_game()

    def hany_kiszallo(self):
        kiszallo, ok = QInputDialog.getInt(self, "Kiszálló", '<html style="font-size: 15px;"> Hány nyílból dobtad meg?</html>', 3, 1, 3)
        if ok and kiszallo:
            return kiszallo
        else:
            return 3

    def pont_beirva(self):
        if self.akt_score == 'score_1':
            if (int(self.current.text()) == 0) or (int(self.current.text()) + 1 == int(self.pont1.text())) or (int(self.current.text()) > int(self.pont1.text())):
                # print("Nulla vagy besokalt")
                self.check_kiszallo(self.player1_id, self.pont1.text())
                write_score = 0
                self.update_score_avg(self.player1_id, write_score, 3)
                self.current.setText("")
                self.kovetkezo_jatekos(write_score, 3)
                if self.leg_kezd == 'player2':
                    self.round_number += 1
            elif (int(self.current.text()) + 1 < int(self.pont1.text())):
                # print("érvényes dobás")
                self.pont1.setText(str(int(self.pont1.text()) - int(self.current.text())))
                self.check_kiszallo(self.player1_id, self.pont1.text())
                write_score = int(self.current.text())
                self.update_score_avg(self.player1_id, write_score, 3)
                self.current.setText("")
                self.kovetkezo_jatekos(write_score, 3)
                if self.leg_kezd == 'player2':
                    self.round_number += 1
            else:
                # print("megdobta")
                self.pont1.setText("0")
                write_score = int(self.current.text())
                nyil = self.hany_kiszallo()
                self.update_score_avg(self.player1_id, write_score, nyil)
                self.update_best_leg_checkout(self.player1_id, write_score, nyil)
                self.dobas(self.player1_id, write_score, nyil)
                self.write_leg(self.player1_id)
                self.won_legs_1 += 1
                self.leg1.setText(str(self.won_legs_1))
                self.kor1.clear()
                self.kor2.clear()
                self.pont1.setText(str(int(self.params[5]) + self.params[8]))
                self.pont2.setText(str(int(self.params[5]) + self.params[9]))
                self.check_kiszallo(self.player1_id, self.pont1.text())
                self.check_kiszallo(self.player2_id, self.pont2.text())
                self.round_number = 1
                self.result_status()
                if self.leg_kezd == "player1":
                    self.leg_kezd = "player2"
                    self.akt_score = "score_2"
                    self.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                    self.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                else:
                    self.leg_kezd = "player1"
                    self.akt_score = "score_1"
                    self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                    self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                self.current.setText("")
                # if self.leg_kezd == 'player2':
                #     self.round_number += 1
        else:
            if (int(self.current.text()) == 0) or (int(self.current.text()) + 1 == int(self.pont2.text())) or (
                    int(self.current.text()) > int(self.pont2.text())):
                self.check_kiszallo(self.player2_id, self.pont2.text())
                write_score = 0
                self.update_score_avg(self.player2_id, write_score, 3)
                self.current.setText("")
                self.kovetkezo_jatekos(write_score, 3)
                if self.leg_kezd == 'player1':
                    self.round_number += 1
            elif (int(self.current.text()) + 1 < int(self.pont2.text())):
                self.pont2.setText(str(int(self.pont2.text()) - int(self.current.text())))
                self.check_kiszallo(self.player2_id, self.pont2.text())
                write_score = int(self.current.text())
                self.update_score_avg(self.player2_id, write_score, 3)
                self.current.setText("")
                self.kovetkezo_jatekos(write_score, 3)
                if self.leg_kezd == 'player1':
                    self.round_number += 1
            else:
                # print("megdobta")
                self.pont2.setText("0")
                write_score = int(self.current.text())
                nyil = self.hany_kiszallo()
                self.update_score_avg(self.player2_id, write_score, nyil)
                self.update_best_leg_checkout(self.player2_id, write_score, nyil)
                self.dobas(self.player2_id, write_score, nyil)
                self.write_leg(self.player2_id)
                self.won_legs_2 += 1
                self.leg2.setText(str(self.won_legs_2))
                self.kor1.clear()
                self.kor2.clear()
                self.pont1.setText(str(int(self.params[5]) + self.params[8]))
                self.pont2.setText(str(int(self.params[5]) + self.params[9]))
                self.check_kiszallo(self.player1_id, self.pont1.text())
                self.check_kiszallo(self.player2_id, self.pont2.text())
                self.round_number = 1
                self.result_status()
                if self.leg_kezd == "player1":
                    self.leg_kezd = "player2"
                    self.akt_score = "score_2"
                    self.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                    self.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                else:
                    self.leg_kezd = "player1"
                    self.akt_score = "score_1"
                    self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                    self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                self.current.setText("")

    def alapertekek(self):
        self.won_legs_1 = 0
        self.won_sets_1 = 0
        self.won_legs_2 = 0
        self.won_sets_2 = 0
        # Számolási adatok
        self.akt_score = 'score_1'
        self.round_number = 1
        self.leg_id = 1
        self.set_id = 1
        self.leg_kezd = "player1"
        self.set_kezd = "player1"
        self.sum_1 = 0
        self.sum_2 = 0
        self.darab_1 = 0
        self.darab_2 = 0
        self.sum9_1 = 0
        self.sum9_2 = 0
        self.darab9_1 = 0
        self.darab9_2 = 0

    def help_felirat(self):
        c0 = CustomHelpLabel("F1: 0")
        self.help_layout.addWidget(c0)
        c1 = CustomHelpLabel("F2: 26")
        self.help_layout.addWidget(c1)
        c2 = CustomHelpLabel("F3: 41")
        self.help_layout.addWidget(c2)
        c3 = CustomHelpLabel("F4: 45")
        self.help_layout.addWidget(c3)
        c4 = CustomHelpLabel("F5: 60")
        self.help_layout.addWidget(c4)
        c5 = CustomHelpLabel("F6: 81")
        self.help_layout.addWidget(c5)
        c6 = CustomHelpLabel("F7: 85")
        self.help_layout.addWidget(c6)
        c7 = CustomHelpLabel("F8: 100")
        self.help_layout.addWidget(c7)
        c8 = CustomHelpLabel("F9: Marad")
        c8.setFixedWidth(95)
        self.help_layout.addWidget(c8)
        c9 = CustomHelpLabel("CTRL-B: Visszavon")
        c9.setFixedWidth(165)
        self.help_layout.addWidget(c9)
        self.help_layout.addStretch(0)

    def set_layouts(self):
        # Fő LAYOUT létrehozása, beállítása
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.nevek_sor = QWidget()
        # self.nevek_sor.setFixedHeight(60)
        self.nevek_sor.setMinimumHeight(80)
        self.nevek_layout = QHBoxLayout()
        self.nevek_sor.setLayout(self.nevek_layout)
        # Az info sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.info_sor = QWidget()
        # self.info_sor.setFixedHeight(100)
        self.info_sor.setMinimumHeight(120)
        self.info_layout = QHBoxLayout()
        self.info_sor.setLayout(self.info_layout)
        # Az checkout sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.checkout_sor = QWidget()
        # self.checkout_sor.setFixedHeight(120)
        self.checkout_sor.setMinimumHeight(220)
        self.checkout_layout = QHBoxLayout()
        self.checkout_sor.setLayout(self.checkout_layout)
        # A státusz sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.statusz_sor = QWidget()
        # self.statusz_sor.setFixedHeight(460)
        self.statusz_sor.setMinimumHeight(380)
        self.statusz_layout = QHBoxLayout()
        self.statusz_sor.setLayout(self.statusz_layout)
        self.help_sor = QWidget()
        self.help_sor.setFixedHeight(35)
        self.help_layout = QHBoxLayout()
        self.help_sor.setLayout(self.help_layout)
        # a PONT1 megjelenítéséhez Widget, layout
        self.score1_widget = QWidget()
        self.score1_widget.setFixedHeight(120)
        self.score1_layout = QVBoxLayout()
        self.score1_widget.setLayout(self.score1_layout)
        # A PONT1 Widget hozzáadása az info LAYOUT-hoz
        self.info_layout.addWidget(self.score1_widget)
        # Set1, Leg1 megjelenítéséhez Widget, Layout
        self.legset1_widget = QWidget()
        self.legset1_widget.setMaximumHeight(120)
        self.legset1_layout = QVBoxLayout()
        self.legset1_widget.setLayout(self.legset1_layout)
        self.leg1_layout = QHBoxLayout()
        self.set1_layout = QHBoxLayout()
        self.legset1_layout.addLayout(self.leg1_layout)
        self.legset1_layout.addLayout(self.set1_layout)
        self.info_layout.addWidget(self.legset1_widget)
        self.legset_widget = QWidget()
        self.legset_widget.setMaximumHeight(120)
        self.legset_layout = QVBoxLayout()
        self.legset_widget.setLayout(self.legset_layout)
        self.info_layout.addWidget(self.legset_widget)
        # Set2, Leg2 megjelenítéséhez Widget, Layout
        self.legset2_widget = QWidget()
        self.legset2_widget.setMaximumHeight(120)
        self.legset2_layout = QVBoxLayout()
        self.legset2_widget.setLayout(self.legset2_layout)
        self.leg2_layout = QHBoxLayout()
        self.set2_layout = QHBoxLayout()
        self.legset2_layout.addLayout(self.leg2_layout)
        self.legset2_layout.addLayout(self.set2_layout)
        self.info_layout.addWidget(self.legset2_widget)
        # a PONT2 megjelenítéséhez Widget, layout
        self.score2_widget = QWidget()
        self.score2_widget.setFixedHeight(120)
        self.score2_layout = QVBoxLayout()
        self.score2_widget.setLayout(self.score2_layout)
        # A PONT2 Widget hozzáadása az info LAYOUT-hoz
        self.info_layout.addWidget(self.score2_widget)
        # a CHEKOUT1 megjelenítéséhez Widget, layout
        self.check1_widget = QWidget()
        self.check1_widget.setFixedHeight(185)
        self.check1_layout = QVBoxLayout()
        self.check1_widget.setLayout(self.check1_layout)
        # A PONT2 Widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.check1_widget, 40)
        # A dobott pont megjelenítéséhez Widget, layout
        self.current_widget = QWidget()
        self.current_widget.setMinimumHeight(210)
        self.current_layout = QVBoxLayout()
        self.current_widget.setLayout(self.current_layout)
        # Az aktuális pont widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.current_widget, 20)
        # a CHEKOUT2 megjelenítéséhez Widget, layout
        self.check2_widget = QWidget()
        self.check2_widget.setFixedHeight(185)
        self.check2_layout = QVBoxLayout()
        self.check2_widget.setLayout(self.check2_layout)
        # A PONT2 Widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.check2_widget, 40)
        # a STAT1 megjelenítéséhez Widget, layout
        self.stat1_widget = QWidget()
        # self.stat1_widget.setFixedHeight(460)
        self.stat1_widget.setMinimumHeight(380)
        self.stat1_layout = QVBoxLayout()
        self.stat1_widget.setLayout(self.stat1_layout)
        # A stat1 Widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.stat1_widget, 20)
        #A körök1 megjelenítéséhez widget, layout
        self.round1_widget = QWidget()
        # self.round1_widget.setFixedHeight(460)
        self.round1_widget.setMinimumHeight(380)
        self.round1_layout = QVBoxLayout()
        self.round1_widget.setLayout(self.round1_layout)
        # A round1 widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.round1_widget, 30)
        # A körök2 megjelenítéséhez widget, layout
        self.round2_widget = QWidget()
        # self.round2_widget.setFixedHeight(460)
        self.round2_widget.setMinimumHeight(380)
        self.round2_layout = QVBoxLayout()
        self.round2_widget.setLayout(self.round2_layout)
        # A round1 widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.round2_widget, 30)
        # a STAT2 megjelenítéséhez Widget, layout
        self.stat2_widget = QWidget()
        # self.stat2_widget.setFixedHeight(460)
        self.stat2_widget.setMinimumHeight(380)
        self.stat2_layout = QVBoxLayout()
        self.stat2_widget.setLayout(self.stat2_layout)
        # A stat2 Widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.stat2_widget, 20)

        # A konténer-widget-ek ( nevek, info-sor, ....) hozzáadása a fő LAYOUT-hoz
        self.layout.addWidget(self.nevek_sor)
        self.layout.addWidget(self.info_sor)
        self.layout.addWidget(self.checkout_sor)
        self.layout.addWidget(self.statusz_sor)
        self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.space)
        self.layout.addWidget(self.help_sor)

    def refresh(self):
        # params.append(player1)
        # params.append(player2)
        # params.append(m_id)
        # params.append(p1_id)
        # params.append(p2_id)
        # params.append(var)
        # params.append(leg)
        # params.append(set)
        # params.append(hc1)
        # params.append(hc2)
        # params.append(bestof)
        # for p in self.params:
        #     print(p)
        self.match_id = self.params[2]
        self.player1_id = self.params[3]
        self.player2_id = self.params[4]
        self.nev1.setText(self.params[0])
        self.nev2.setText(self.params[1])
        self.pont1.setText(str(int(self.params[5]) + self.params[8]))
        self.pont2.setText(str(int(self.params[5]) + self.params[9]))
        self.variant = self.params[5]
        self.bestof = self.params[10]
        self.legsperset = self.params[6]
        self.sets = self.params[7]
        if self.sets == 1:
            self.set1.hide()
            self.set_cimke.hide()
            self.set2.hide()
        else:
            self.bestof = 0
        # print("paraméterek frissítése")
        query = QSqlQuery(f"select * from matches where match_id={self.match_id}")
        query.exec_()
        if query.numRowsAffected():
            darab1 = darab2 = 0
            while query.next():
                if query.value(3) == self.player1_id:
                    darab1 += 1
                else:
                    darab2 += 1
            self.won_legs_1 = darab1
            self.leg1.setText(str(self.won_legs_1))
            self.won_legs_2 = darab2
            self.leg2.setText(str(self.won_legs_2))
            if ((darab1 + darab2) % 2 == 0):
                self.leg_kezd = "player1"
                self.akt_score = 'score_1'
                self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
                self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
            else:
                self.leg_kezd = "player2"
                self.akt_score = 'score_2'
                self.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")
                self.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
        else:
            self.won_legs_1 = 0
            self.leg1.setText(str(self.won_legs_1))
            self.won_legs_2 = 0
            self.leg2.setText(str(self.won_legs_2))
            self.leg_kezd = "player1"
            self.akt_score = 'score_1'
            self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 90px")
            self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 90px")

if __name__ == '__main__':
    app = QApplication([])
    win = GameWindowDialog()
    win.show()
    app.exec_()
