from PySide2.QtWidgets import QListWidget, QListWidgetItem, QLabel, QDialog, QApplication, QScrollArea, QVBoxLayout, QGridLayout, QWidget
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel
from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PySide2.QtCore import *
import sys

# db = QSqlDatabase.addDatabase('QSQLITE')
# db.setDatabaseName('scorer.db3')
# Ha a progiból indul, nem kell majd
# if not db.open():
#     QMessageBox.critical(
#         None,
#         "App Name - Error!",
#         "Database Error: %s" % db.lastError().text(),
#     )
#     sys.exit(1)


class MatchStatWindow(QDialog):
    def __init__(self, parent=None):
        super(MatchStatWindow, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Mérkőzés választása")
        self.resize(740, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.merkozesek = QListWidget()
        self.merkozesek.setFixedHeight(200)
        self.merkozesek.setFixedWidth(730)
        self.merkozesek.itemDoubleClicked.connect(self.stat_game)
        self.layout.addWidget(self.merkozesek)
        self.szumma = MatchSumWidget(self)
        self.layout.addWidget(self.szumma)
        self.history = QWidget()
        self.history.setFixedWidth(690)
        self.history_layout = QGridLayout()
        self.history.setLayout(self.history_layout)
        scroll = QScrollArea()
        scroll.setWidget(self.history)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        self.match_valasztas()

    def match_valasztas(self):
        matches = QSqlQueryModel()
        matches_query = QSqlQuery("SELECT a.match_id, c.player_name as nev1, d.player_name as nev2, a.variant, a.sets, \
                          a.legsperset, a.hc1, a.hc2, a.timestamp FROM match_settings a, players c, players d \
                            WHERE a.player1_id=c.player_id and a.player2_id=d.player_id ORDER BY `a`.timestamp DESC")
        matches.setQuery(matches_query)
        self.merkozesek.clear()
        fejlec = QListWidgetItem(f'Név1\tNév2\tPont1\tPont2\tLegs\tSets\tDátum\tMeccs_ID')
        betuk = fejlec.font()
        betuk.setBold(True)
        fejlec.setFont(betuk)
        self.merkozesek.addItem(fejlec)
        for i in range(matches.rowCount()):
            self.merkozesek.addItem(matches.record(i).value(1) + "\t" +
                                    matches.record(i).value(2) + "\t" +
                                    str(int(matches.record(i).value(3)) + matches.record(i).value(6)) + "\t" +
                                    str(int(matches.record(i).value(3)) + matches.record(i).value(7)) + "\t" +
                                    str(matches.record(i).value(4)) + "\t" +
                                    str(matches.record(i).value(5)) + "\t" +
                                    str(matches.record(i).value(8).toString('yyyy MM dd')) + "\t" +
                                    str(matches.record(i).value(0))
                                    )

    def stat_game(self):
        # Az átvett adatok:
        para = self.merkozesek.currentItem().text().rsplit("\t")
        # Összegyűjtjük egy listába a szükséges infókat
        self.get_adatok(para)
        self.szumma.change_data(self.adatok)
        for x in reversed(range(self.history_layout.count())):
            self.history_layout.itemAt(x).widget().deleteLater()
        # kiszedjük az adott meccs összes set és leg esetére a dobásokat
        sor = 0
        for s in range(1, self.adatok[8] + 1):
            # s: a set-ek száma
            if self.adatok[8] != 1:
                self.history_layout.addWidget(QLabel("Set: " + str(s)), sor, 0, 1, 2)
                sor += 1
            for l in range(1, self.adatok[7][s-1] + 1):
                sl1_model = QSqlQueryModel()
                p1_data_list = []
                p1_data_list.append(self.adatok[4])   # start_score1
                sl1_query = QSqlQuery(f"select * from dobas where match_id ={self.adatok[6]} and set_id={s} and leg_id={l} and player_id='{self.adatok[0]}'", db=db)
                sl1_model.setQuery(sl1_query)
                for i in range(sl1_model.rowCount()):
                    # Itt a model már tartalmazza a p1 összes dobását az adott leg-ben.
                    p1_data_row = []
                    p1_data_row.append(sl1_model.record(i).value(1))
                    p1_data_row.append(sl1_model.record(i).value(2))
                    p1_data_list.append(p1_data_row)
                self.history_layout.addWidget(PlayerLegWidget(self, p1_data_list), sor, 0, Qt.AlignTop)

                sl2_model = QSqlQueryModel()
                p2_data_list = []
                p2_data_list.append(self.adatok[5])  # start_score2
                sl2_query = QSqlQuery(f"select * from dobas where match_id ={self.adatok[6]} and set_id={s} and leg_id={l} and player_id='{self.adatok[2]}'", db=db)
                sl2_model.setQuery(sl2_query)
                for j in range(sl2_model.rowCount()):
                    p2_data_row = []
                    p2_data_row.append(sl2_model.record(j).value(1))
                    p2_data_row.append(sl2_model.record(j).value(2))
                    p2_data_list.append(p2_data_row)
                self.history_layout.addWidget(PlayerLegWidget(self, p2_data_list), sor, 1, Qt.AlignTop)
                sor += 1

    def get_adatok(self, para):
        print(para)
        # self.adatok[0]  : p1_id
        # self.adatok[1]  : name1
        # self.adatok[2]  : p2_id
        # self.adatok[3]  : name2
        # self.adatok[4]  : start_score1
        # self.adatok[5]  : start_score2
        # self.adatok[6]  : match
        # self.adatok[7]  : legs
        # self.adatok[8]  : sets
        # self.adatok[9]  : dátum

        self.adatok = []
        name1_id = int(para[0])
        self.adatok.append(name1_id)
        query_name1 = QSqlQuery(f"select player_name from players where player_id={name1_id}", db=db)
        query_name1.exec_()
        while query_name1.next():
            name1 = query_name1.value(0)
        self.adatok.append(name1)
        name2_id = int(para[1])
        self.adatok.append(name2_id)
        query_name2 = QSqlQuery(f"select player_name from players where player_id={name2_id}", db=db)
        query_name2.exec_()
        while query_name2.next():
            name2 = query_name2.value(0)
        self.adatok.append(name2)

        start_score1 = int(para[2])
        start_score2 = int(para[3])
        match = int(para[7])
        setek = int(para[5])
        self.adatok.append(start_score1)
        self.adatok.append(start_score2)
        self.adatok.append(match)
        # Kell a max set-number, ezt beállítani a sets változóba
        # Ciklussal minden set-ben megnézni a max leg-numbert, és ezeket append-elni a legs[]-hez
        # Végül leg, set sorrendben append-elni az adatokhoz
        legs = []
        sets = 0
        query2 = QSqlQuery(
            f"select max(set_id) as max_set from matches where match_id={match}", db=db)
        query2.exec_()
        while query2.next():
            sets = int(query2.value(0))

        for i in range(1, sets + 1):
            query = QSqlQuery(f"select max(leg_id) as max_leg from matches where match_id={match} and set_id={i}", db=db)
            query.exec_()
            while query.next():
                legs.append(int(query.value(0)))
                # sets.append(int(query.value(1)))

        self.adatok.append(legs)
        self.adatok.append(sets)

        datum = para[6][:16]
        self.adatok.append(datum)
        print(self.adatok)


class MatchSumWidget(QWidget):
    def __init__(self, parent):
        super(MatchSumWidget, self).__init__(parent)
        self.parent = parent
        self.painter = QPainter()
        self.data = None
        self.setFixedSize(730, 70)

    def change_data(self, szum=None):
        self.data = None
        self.data = szum
        self.name1 = self.data[1]
        self.name2 = self.data[3]
        match_id = self.data[6]
        p1_id = self.data[0]
        p2_id = self.data[2]
        # Végeredmény
        self.won1 = 0
        self.won2 = 0
        self.avg1 = self.avg2 = 0
        eredmenyek_model = QSqlQueryModel()
        eredmenyek_query = QSqlQuery(f"select * from matches where match_id={match_id}", db=db)
        eredmenyek_model.setQuery(eredmenyek_query)
        for x in range(1, self.data[8] + 1):
            l1 = l2 = 0
            for i in range(eredmenyek_model.rowCount()):  # csak set-eket összesítünk
                if eredmenyek_model.record(i).value(2) == x:
                    if eredmenyek_model.record(i).value(3) == p1_id:
                        l1 += 1
                    else:
                        l2 += 1
            # print("Set: ", x, "L1: ", l1, "L2: ", l2)
            if self.data[8] == 1:
                self.won1 = l1
                self.won2 = l2
            else:
                if l1 > l2:
                    self.won1 += 1
                else:
                    self.won2 += 1
        # Átlagok
        db1 = db2 = sum1 = sum2 = 0
        for x in range(1, self.data[8] + 1):
            for leg in range(1, self.data[7][x - 1] + 1):
                query = QSqlQuery(f"select max(round_number) as maxround, sum(points) as sumpont from dobas where leg_id={leg} and set_id={x} and match_id={match_id} and player_id={p1_id}")
                query.exec_()
                while query.next():
                    db1 += query.value(0)
                    sum1 += query.value(1)
                query2 = QSqlQuery(f"select max(round_number) as maxround, sum(points) as sumpont from dobas where leg_id={leg} and set_id={x} and match_id={match_id} and player_id={p2_id}")
                query2.exec_()
                while query2.next():
                    db2 += query2.value(0)
                    sum2 += query2.value(1)
        self.avg1 = round(sum1 / db1 * 3, 2)
        self.avg2 = round(sum2 / db2 * 3, 2)

        self.update()

    def paintEvent(self, event):
        if self.data:
            self.painter.begin(self)
            brush_alap = QBrush(QColor(220, 220, 220))
            self.painter.setBrush(brush_alap)
            self.painter.drawRect(0, 0, 728, 68)
            nev_font = QFont('Times', 18)
            nev_pen = QPen(QColor(168, 34, 3))
            self.painter.setFont(nev_font)
            self.painter.setPen(nev_pen)
            self.painter.drawText(10, 30, self.name1)
            self.painter.drawText(500, 30, self.name2)
            ered_font = QFont('Times', 14)
            ered_pen = QPen(QColor(168, 34, 93))
            self.painter.setPen(ered_pen)
            self.painter.setFont(ered_font)
            self.painter.drawText(270, 30, str(self.won1))
            self.painter.drawText(400, 30, str(self.won2))
            self.painter.drawText(50, 60, "(" + str(self.avg1) + ")")
            self.painter.drawText(540, 60, "(" + str(self.avg2) + ")")
            self.painter.drawText(250, 60, "(" + str(self.data[4]) + ")")
            self.painter.drawText(380, 60, "(" + str(self.data[5]) + ")")
            self.painter.end()

class PlayerLegWidget(QWidget):
    def __init__(self, parent, data):
        super(PlayerLegWidget, self).__init__(parent)
        self.parent = parent
        self.data = data
        self.setFixedHeight((len(self.data)) * 20)
        self.painter = QPainter()

    def paintEvent(self, event):
        self.painter.begin(self)
        maradek = self.data[0]
        self.painter.drawRect(0, 0, 330, self.height() - 5)
        pen = QPen(QColor(0, 0, 255))
        self.painter.setPen(pen)
        for i in range(1, len(self.data)):
            self.painter.drawText(50, i * 20, str(self.data[i][0]))
            self.painter.drawText(100, i * 20, "|")
            self.painter.drawText(130, i * 20, str(self.data[i][1]))
            self.painter.drawText(180, i * 20, "|")
            maradek -= self.data[i][1]
            self.painter.drawText(210, i * 20, str(maradek))
        self.painter.end()

if __name__ == '__main__':
    app = QApplication([])
    win = MatchStatWindow()
    win.show()
    app.exec_()