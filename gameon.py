from PySide2.QtWidgets import QSpacerItem, QWidget, QMessageBox, QDialog, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy, QTextEdit
from PySide2.QtCore import *
from PySide2.QtGui import QRegExpValidator, QIntValidator
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel


db = QSqlDatabase.addDatabase('QMYSQL')
db.setHostName('localhost')
db.setDatabaseName('cida')
db.setUserName('cida')
db.setPassword('cida')

if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)


class GameWindowDialog(QDialog):
    def __init__(self, parent = None):
        super(GameWindowDialog, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.resize(1000, 800)

        self.params = []
        self.set_layouts()
        self.alapertekek()
        # A neveket tartalmazó QLabel-ek létrehozása, hozzáadása a neveket tartalmazó layout-hoz
        self.nev1 = QLabel()
        self.nev1.setAlignment(Qt.AlignCenter)
        self.nev1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 35px; font-family: Cuorier New")
        self.nev2 = QLabel()
        self.nev2.setAlignment(Qt.AlignCenter)
        self.nev2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 35px; font-family: Cuorier New")
        self.nevek_layout.addWidget(self.nev1)
        self.nevek_layout.addWidget(self.nev2)
        # A konkrét pontszámot tartalmazó widget hozzáadása a pont1 widget layout-jához
        self.pont1 = QLabel("501")
        self.pont1.setAlignment(Qt.AlignCenter)
        self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 75px")
        self.score1_layout.addWidget(self.pont1)
        # Set1, Leg1 megjelenítéséhez Widget, Layout
        self.leg1_layout.addWidget(QLabel("Leg:"))
        self.leg1 = QLabel("0")
        self.leg1_layout.addWidget(self.leg1)
        self.set1_layout.addWidget(QLabel("Set:"))
        self.set1 = QLabel("0")
        self.set1_layout.addWidget(self.set1)
        # Set2, Leg2 megjelenítéséhez Widget, Layout
        self.leg2_layout.addWidget(QLabel("Leg:"))
        self.leg2 = QLabel("0")
        self.leg2_layout.addWidget(self.leg2)
        self.set2_layout.addWidget(QLabel("Set:"))
        self.set2 = QLabel("0")
        self.set2_layout.addWidget(self.set2)
        # A konkrét pontszámot tartalmazó widget hozzáadása a pont2 widget layout-jához
        self.pont2 = QLabel("501")
        self.pont2.setAlignment(Qt.AlignCenter)
        self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 75px")
        self.score2_layout.addWidget(self.pont2)
        # A CHEKOUT1-ET tartalmazó Widget hozzáadása a checkout1 widget layout-jához
        self.check1 = QLabel("Check-Out 1")
        self.check1.setAlignment(Qt.AlignCenter)
        self.check1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 30px")
        self.check1_layout.addWidget(self.check1)
        # A CHEKOUT2-ET tartalmazó Widget hozzáadása a checkout2 widget layout-jához
        self.check2 = QLabel("Check-Out 2")
        self.check2.setAlignment(Qt.AlignCenter)
        self.check2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 30px")
        self.check2_layout.addWidget(self.check2)
        # Az aktuális pontszámot tartalmazó Widget hozzáadása a current widget layout-jához
        validator = QIntValidator(0,180)
        self.current = QLineEdit()
        self.current.setValidator(validator)
        self.current.setFocus()
        self.current.setAlignment(Qt.AlignCenter)
        self.current.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 50px")
        self.current_layout.addWidget(self.current)
        self.current.returnPressed.connect(self.pont_beirva)
        # A statisztika1-et tartalmazo widget hozzáadása a stat1 layout-hoz
        self.stat1 = QTextEdit()
        self.stat1.setAlignment(Qt.AlignLeft)
        self.stat1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 20px")
        self.stat1_layout.addWidget(self.stat1)
        # A statisztika2-et tartalmazo widget hozzáadása a stat2 layout-hoz
        self.stat2 = QTextEdit()
        self.stat2.setAlignment(Qt.AlignLeft)
        self.stat2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 20px")
        self.stat2_layout.addWidget(self.stat2)
        # A körök1-et tartalmazo widget hozzáadása a korok1 layout-hoz
        self.kor1 = QTextEdit()
        self.kor1.setAlignment(Qt.AlignCenter)
        self.kor1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 20px")
        self.round1_layout.addWidget(self.kor1)
        # A körök2-et tartalmazo widget hozzáadása a korok2 layout-hoz
        self.kor2 = QTextEdit()
        self.kor2.setAlignment(Qt.AlignCenter)
        self.kor2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 20px")
        self.round2_layout.addWidget(self.kor2)

    def dobas(self, player, score):
        """
        Az aktuális,érvényes dobás beszúrása a dobas táblába.
        [player_id(player), round_number, points(score), leg_id, set_id, match_id, timestamp]
        :param player:
        :param score:
        :return:
        """
        # print("Dobás rögzítése")
        now = QDateTime.currentDateTime()
        dobas_model = QSqlTableModel()
        dobas_model.setTable("dobas")
        record = dobas_model.record()
        record.setValue(0, player)
        record.setValue(1, self.round_number)
        record.setValue(2, score)
        record.setValue(3, self.leg_id)
        record.setValue(4, self.set_id)
        record.setValue(5, self.match_id)
        record.setValue(6, now)
        # print(record)
        if dobas_model.insertRecord(-1, record):
            dobas_model.submitAll()
            # dobas_model = None
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
        record.setValue(6, now)
        print(record)
        if leg_model.insertRecord(-1, record):
            leg_model.submitAll()
            # dobas_model = None
        else:
            db.rollback()

    def kovetkezo_jatekos(self, write_score):
        # print("következő játékos")
        if self.akt_score == 'score_1':
            self.dobas(self.player1_id, write_score)
            self.kor1.append(str(3 * self.round_number) + ":\t" + str(write_score) + "\t" + self.pont1.text())
            self.akt_score = 'score_2'
            self.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 60px")
            self.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 60px")
        else:
            self.dobas(self.player2_id, write_score)
            self.kor2.append(str(3 * self.round_number) + ":\t" + str(write_score) + "\t" + self.pont2.text())
            self.akt_score = 'score_1'
            self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 60px")
            self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 60px")

    def result_staus(self):
        """
                self.setperleg: Hány Leg-et kell nyerni 1 Set-hez
                self.sets: Hány Set-et kell nyerni a meccs-hez
                self.leg_id: Hányadik Leg az adott Set-ben
                self.set_id: Hányadik Set az adott meccs-ben
        """
        # db1: az adott mecs, adott set-
        pass

    def pont_beirva(self):
        # print(self.pont1.text())
        # print(self.current.text())
        # self.current.setText("")
        if self.akt_score == 'score_1':
            if (int(self.current.text()) == 0) or (int(self.current.text()) + 1 == int(self.pont1.text())) or (int(self.current.text()) > int(self.pont1.text())):
                print("Nulla vagy besokalt")
                write_score = 0
                self.current.setText("")
                self.kovetkezo_jatekos(write_score)
                if self.leg_kezd == 'player2':
                    self.round_number += 1
            elif (int(self.current.text()) + 1 < int(self.pont1.text())):
                print("érvényes dobás")
                self.pont1.setText(str(int(self.pont1.text()) - int(self.current.text())))
                write_score = int(self.current.text())
                self.current.setText("")
                self.kovetkezo_jatekos(write_score)
                if self.leg_kezd == 'player2':
                    self.round_number += 1
            else:
                print("megdobta")
                self.pont1.setText("0")
                write_score = int(self.current.text())
                self.dobas(self.player1_id, write_score)
                self.write_leg(self.player1_id)
                self.won_legs_1 += 1
                self.leg1.setText(str(self.won_legs_1))
                self.kor1.clear()
                self.kor2.clear()
                self.pont1.setText(self.params[5])
                self.pont2.setText(self.params[5])
                self.round_number = 1
                self.result_status()
                if self.leg_kezd == "player1":
                    self.leg_kezd = "player2"
                    self.akt_score = "score_2"
                    self.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 75px")
                    self.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 75px")
                else:
                    self.leg_kezd = "player1"
                    self.akt_score = "score_1"
                    self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 75px")
                    self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 75px")
                self.current.setText("")
                # if self.leg_kezd == 'player2':
                #     self.round_number += 1
        else:
            if (int(self.current.text()) == 0) or (int(self.current.text()) + 1 == int(self.pont2.text())) or (
                    int(self.current.text()) > int(self.pont2.text())):
                write_score = 0
                self.current.setText("")
                self.kovetkezo_jatekos(write_score)
                if self.leg_kezd == 'player1':
                    self.round_number += 1
            elif (int(self.current.text()) + 1 < int(self.pont2.text())):
                self.pont2.setText(str(int(self.pont2.text()) - int(self.current.text())))
                write_score = int(self.current.text())
                self.current.setText("")
                self.kovetkezo_jatekos(write_score)
                if self.leg_kezd == 'player1':
                    self.round_number += 1
            else:
                print("megdobta")
                self.pont2.setText("0")
                write_score = int(self.current.text())
                self.dobas(self.player2_id, write_score)
                self.write_leg(self.player2_id)
                self.won_legs_2 += 1
                self.leg2.setText(str(self.won_legs_2))
                self.kor1.clear()
                self.kor2.clear()
                self.pont1.setText(self.params[5])
                self.pont2.setText(self.params[5])
                self.round_number = 1
                self.result_status()
                if self.leg_kezd == "player1":
                    self.leg_kezd = "player2"
                    self.akt_score = "score_2"
                    self.pont1.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 75px")
                    self.pont2.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 75px")
                else:
                    self.leg_kezd = "player1"
                    self.akt_score = "score_1"
                    self.pont1.setStyleSheet("background-color: lightgreen; border-radius: 5px; font-size: 75px")
                    self.pont2.setStyleSheet("background-color: lightgray; border-radius: 5px; font-size: 75px")
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

    def set_layouts(self):
        # Fő LAYOUT létrehozása, beállítása
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Legfelső sor (nevek) Widget max magassággal, hozzárendelve egy LAYOUT, amihez hozzáadjuk a neveket
        self.nevek_sor = QWidget()
        self.nevek_sor.setFixedHeight(60)
        self.nevek_layout = QHBoxLayout()
        self.nevek_sor.setLayout(self.nevek_layout)
        # Az info sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.info_sor = QWidget()
        self.info_sor.setFixedHeight(100)
        self.info_layout = QHBoxLayout()
        self.info_sor.setLayout(self.info_layout)
        # Az checkout sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.checkout_sor = QWidget()
        self.checkout_sor.setFixedHeight(100)
        self.checkout_layout = QHBoxLayout()
        self.checkout_sor.setLayout(self.checkout_layout)
        # A státusz sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.statusz_sor = QWidget()
        self.statusz_sor.setFixedHeight(500)
        self.statusz_layout = QHBoxLayout()
        self.statusz_sor.setLayout(self.statusz_layout)
        # a PONT1 megjelenítéséhez Widget, layout
        self.score1_widget = QWidget()
        self.score1_widget.setFixedHeight(100)
        self.score1_layout = QVBoxLayout()
        self.score1_widget.setLayout(self.score1_layout)
        # A PONT1 Widget hozzáadása az info LAYOUT-hoz
        self.info_layout.addWidget(self.score1_widget)
        # Set1, Leg1 megjelenítéséhez Widget, Layout
        self.legset1_widget = QWidget()
        self.legset1_widget.setMaximumHeight(100)
        self.legset1_layout = QVBoxLayout()
        self.legset1_widget.setLayout(self.legset1_layout)
        self.leg1_layout = QHBoxLayout()
        self.set1_layout = QHBoxLayout()
        self.legset1_layout.addLayout(self.leg1_layout)
        self.legset1_layout.addLayout(self.set1_layout)
        self.info_layout.addWidget(self.legset1_widget)
        # Set2, Leg2 megjelenítéséhez Widget, Layout
        self.legset2_widget = QWidget()
        self.legset2_widget.setMaximumHeight(100)
        self.legset2_layout = QVBoxLayout()
        self.legset2_widget.setLayout(self.legset2_layout)
        self.leg2_layout = QHBoxLayout()
        self.set2_layout = QHBoxLayout()
        self.legset2_layout.addLayout(self.leg2_layout)
        self.legset2_layout.addLayout(self.set2_layout)
        self.info_layout.addWidget(self.legset2_widget)
        # a PONT2 megjelenítéséhez Widget, layout
        self.score2_widget = QWidget()
        self.score2_widget.setFixedHeight(100)
        self.score2_layout = QVBoxLayout()
        self.score2_widget.setLayout(self.score2_layout)
        # A PONT2 Widget hozzáadása az info LAYOUT-hoz
        self.info_layout.addWidget(self.score2_widget)
        # a CHEKOUT1 megjelenítéséhez Widget, layout
        self.check1_widget = QWidget()
        self.check1_widget.setFixedHeight(100)
        self.check1_layout = QVBoxLayout()
        self.check1_widget.setLayout(self.check1_layout)
        # A PONT2 Widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.check1_widget, 42)
        # A dobott pont megjelenítéséhez Widget, layout
        self.current_widget = QWidget()
        self.current_widget.setFixedHeight(100)
        self.current_layout = QVBoxLayout()
        self.current_widget.setLayout(self.current_layout)
        # Az aktuális pont widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.current_widget, 16)
        # a CHEKOUT2 megjelenítéséhez Widget, layout
        self.check2_widget = QWidget()
        self.check2_widget.setFixedHeight(100)
        self.check2_layout = QVBoxLayout()
        self.check2_widget.setLayout(self.check2_layout)
        # A PONT2 Widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.check2_widget, 42)
        # a STAT1 megjelenítéséhez Widget, layout
        self.stat1_widget = QWidget()
        self.stat1_widget.setFixedHeight(500)
        self.stat1_layout = QVBoxLayout()
        self.stat1_widget.setLayout(self.stat1_layout)
        # A stat1 Widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.stat1_widget, 20)
        #A körök1 megjelenítéséhez widget, layout
        self.round1_widget = QWidget()
        self.round1_widget.setFixedHeight(500)
        self.round1_layout = QVBoxLayout()
        self.round1_widget.setLayout(self.round1_layout)
        # A round1 widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.round1_widget, 30)
        # A körök2 megjelenítéséhez widget, layout
        self.round2_widget = QWidget()
        self.round2_widget.setFixedHeight(500)
        self.round2_layout = QVBoxLayout()
        self.round2_widget.setLayout(self.round2_layout)
        # A round1 widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.round2_widget, 30)
        # a STAT2 megjelenítéséhez Widget, layout
        self.stat2_widget = QWidget()
        self.stat2_widget.setFixedHeight(500)
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

    def refresh(self):
        # params.append(player1)
        # params.append(player2)
        # params.append(m_id)
        # params.append(p1_id)
        # params.append(p2_id)
        # params.append(var)
        # params.append(set)
        # params.append(leg)
        self.match_id = self.params[2]
        self.player1_id = self.params[3]
        self.player2_id = self.params[4]
        self.nev1.setText(self.params[0])
        self.nev2.setText(self.params[1])
        self.pont1.setText(self.params[5])
        self.pont2.setText(self.params[5])
        self.setperleg = self.params[6]
        self.sets= self.params[7]


if __name__ == '__main__':
    app = QApplication([])
    win = GameWindowDialog()
    win.show()
    app.exec_()