from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QListWidget, \
    QListWidgetItem, QPushButton, QDialog, QLabel, QMessageBox
from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QDrag
from PySide2.QtCore import Qt, QMimeData, QDataStream, QIODevice, QByteArray
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
import sys

db = QSqlDatabase.addDatabase('QMYSQL')
db.setHostName('192.168.68.22')
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

torna_id = 8889
# csoportok_szama = 0  # todo torna_settings-ből lekérni a 'csoportok_szama' ahol a torna_id a megadott
# sorok_szama = 0 # todo torna_settings-ből lekérni a 'fo_per_csoport' ahol a torna_id a megadott
csoport_tabla = [6, 5, 5, 6] # todo ez sem a settings-ben, sem a torna_tablakban nincs rögzítve(a torna_match tartalmazza, ott viszont a csoport száma nincs


class TornaStatuszWindow(QDialog):
    def __init__(self, parent=None):
        super(TornaStatuszWindow, self).__init__(parent)
        self.setWindowTitle("Torna állása")
        self.get_params()
        self.create_widgets()
        self.set_layout()

    def get_params(self):
        query = QSqlQuery(f"select * from torna_settings where torna_id={torna_id}")
        query.exec_()
        query.first()
        self.csoportok_szama = query.value(3)
        self.sorok_szama = query.value(4)
        self.nyereshez_kell = query.value(8)
        self.pont_gyozelem = query.value(11)
        self.pont_vereseg = query.value(13)
        print("nyeréshez kell: ", self.nyereshez_kell)
        self.tablak = []
        for cs in range(self.csoportok_szama):
            tablasor = []
            for sor in range(self.sorok_szama):
                tablasor.append(0)
            self.tablak.append(tablasor)
        query2 = QSqlQuery(f"select * from torna_tablak where torna_id={torna_id}")
        query2.exec_()
        while query2.next():
            self.tablak[query2.value(2)][query2.value(3)] = query2.value(1)
        self.nevek = []
        for cs in range(self.csoportok_szama):
            neveksor = []
            for sor in range(self.sorok_szama):
                neveksor.append("")
            self.nevek.append(neveksor)
        query2 = QSqlQuery(f"select player_id, player_name from torna_resztvevok where torna_id={torna_id}")
        query2.exec_()
        while query2.next():
            for x in range(self.csoportok_szama):
                for y in range(self.sorok_szama):
                    if query2.value(0) == self.tablak[x][y]:
                        self.nevek[x][y] = query2.value(1)
        print(self.tablak, self.nevek)

    def create_widgets(self):
        # GroupMemberWidget-ek
        self.csoportok = []
        for i in range(self.csoportok_szama):  # Csoportok száma
            self.csoportoszlop = []
            for j in range(self.sorok_szama):  # fő/csoport
                self.csoportoszlop.append(GroupMemberWidget(self))
                self.csoportoszlop[j]._set_csoport_number(i)
                self.csoportoszlop[j]._set_csoport_sor(j)
                self.csoportoszlop[j]._set_player_id(self.tablak[i][j])
                self.csoportoszlop[j]._set_player_name(self.nevek[i][j])
            self.csoportok.append(self.csoportoszlop)

        # EredmenyWidget-ek
        self.eredmenyek = []
        for i in range(self.csoportok_szama):
            self.csoport_eredmeny_matrix = []
            for j in range(self.sorok_szama):  # ami egyenlő az oszlopok számával!!!
                self.eredmeny_oszlop = []
                for x in range(self.sorok_szama):
                    self.eredmeny_oszlop.append(EredmenyWidget(self))
                    self.eredmeny_oszlop[x]._set_csoport_number(i)
                    self.eredmeny_oszlop[x]._set_csoport_sor(j)
                    self.eredmeny_oszlop[x]._set_csoport_oszlop(x)
                    self.eredmeny_oszlop[x]._set_p1_id(self.tablak[i][j])
                    self.eredmeny_oszlop[x]._set_p2_id(self.tablak[i][x])

                self.csoport_eredmeny_matrix.append(self.eredmeny_oszlop)
            self.eredmenyek.append(self.csoport_eredmeny_matrix)

        # SzumWidget-ek
        self.szum_eredmenyek = []
        for i in range(self.csoportok_szama):  # 2
            self.csoport_szum_eredmeny_matrix = []
            for j in range(5):  # ami egyenlő az oszlopok számával!!!
                self.szum_eredmeny_oszlop = []
                for x in range(self.sorok_szama):
                    self.szum_eredmeny_oszlop.append(SzumWidget(self))
                    # self.eredmeny_oszlop[x]._set_csoport_number(i)
                    # self.eredmeny_oszlop[x]._set_csoport_sor(x)
                    # self.eredmeny_oszlop[x]._set_csoport_oszlop(j)
                    self.szum_eredmeny_oszlop[x]._set_p_id(self.tablak[i][x])
                    # self.eredmeny_oszlop[x]._set_p2_id(self.tablak[i][x])

                self.csoport_szum_eredmeny_matrix.append(self.szum_eredmeny_oszlop)
            self.szum_eredmenyek.append(self.csoport_szum_eredmeny_matrix)

        self.refresh_button = QPushButton("Frissítés")
        self.refresh_button.clicked.connect(self.update_statusz)

    def set_layout(self):
        main_layout = QHBoxLayout()
        groups = QWidget()
        groups.setFixedWidth(((self.sorok_szama + 5) * 50) + 200 )
        widgets_layout = QVBoxLayout()
        groups.setLayout(widgets_layout)

        for n in range(self.csoportok_szama): # csoportok száma
            locals()['csoport_layout' + str(n)] = QGridLayout() # Létrehozzuk az adott sorszámú csoport layout-ját
            locals()['csoport_layout' + str(n)].setContentsMargins(0, 0, 0, 0)
            locals()['csoport_layout' + str(n)].setHorizontalSpacing(0)
            locals()['csoport_layout' + str(n)].setVerticalSpacing(0)
            widgets_layout.addLayout(locals()['csoport_layout' + str(n)]) # Hozzáadjuk a a layout-ot a widget_layout-hoz
            locals()['csoport_layout' + str(n)].addWidget(QLabel("Csoport_" + str(n + 1)), 0, 0, Qt.AlignHCenter)
            sorok = len(self.csoportok[n])
            for k in range(sorok):
                locals()['csoport_layout' + str(n)].addWidget(QLabel(str(k + 1)), 0, k + 1, Qt.AlignHCenter)
            locals()['csoport_layout' + str(n)].addWidget(QLabel("NY"), 0, sorok + 5, Qt.AlignHCenter)
            locals()['csoport_layout' + str(n)].addWidget(QLabel("V"), 0, sorok + 6, Qt.AlignHCenter)
            locals()['csoport_layout' + str(n)].addWidget(QLabel("K"), 0, sorok + 7, Qt.AlignHCenter)
            locals()['csoport_layout' + str(n)].addWidget(QLabel("P"), 0, sorok + 8, Qt.AlignHCenter)
            locals()['csoport_layout' + str(n)].addWidget(QLabel("H"), 0, sorok + 9, Qt.AlignHCenter)
            for i in range(len(self.csoportok[n])):  # len(self.csoportok[n]) : csoporton belüli sorok száma
            # Végigmegyünk a sorokon   :  i: sorok száma, n: csoport száma

                # N: HÁNYADIK CSOPORT, I: HÁNYADIK OSZLOP-OT TÖLTJÜK
                # a layout 1. oszlopát feltöltjük a tömbben tárolt custom widget-ekkel
                # self.csoportok[n][i] N-EDIK CSOPORT I-DIK SORÁBAN A NÉV
                locals()['csoport_layout' + str(n)].addWidget(self.csoportok[n][i], i + 1, 0)
                # Itt töltjük fel az eredmény-widget-eket, és a szummákat (tombben tárolva, mint a GroupMemberWidget-ek)
                # eredmenyek[n, y, i] n: csoport, y: oszlop, i: sor
                for x in range(len(self.csoportok[n])): # Ez lesz az oszlop(max = sorok száma) x: oszlop száma
                    locals()['csoport_layout' + str(n)].addWidget(self.eredmenyek[n][i][x], i + 1, x + 1)
                # szum_eredmenyek[x, y, z] x: csoport, y: oszlop, z: sor
                for y in range(5):  # 5 kockát rakunk ki
                    locals()['csoport_layout' + str(n)].addWidget(self.szum_eredmenyek[n][y][i], i + 1, 5 + x +y + 1)

            # locals()['csoport_layout' + str(n)].addWidget(QLabel("Csoport_" + str(n + 1)), 0, 0)

        lista_layout = QVBoxLayout()
        lista_layout.addWidget(self.refresh_button)

        scroll = QScrollArea()
        scroll.setWidget(groups)
        scroll.setFixedWidth(((self.sorok_szama + 5) * 50) + 220)
        scroll.setFixedHeight(740)

        main_layout.addWidget(scroll)
        main_layout.addLayout(lista_layout)
        self.setLayout(main_layout)

    def update_statusz(self):
        legek = []
        query = QSqlQuery(f"SELECT matches.*,torna_match.player1_id as p1,torna_match.player2_id as p2 FROM matches,\
         torna_match WHERE matches.match_id=torna_match.match_id and torna_match.torna_id={torna_id}")
        query.exec_()
        while query.next():
            akt_leg = []
            akt_leg.append(query.value(0)) # match_id
            akt_leg.append(query.value(5)) # p1
            akt_leg.append(query.value(6)) # p2
            akt_leg.append(query.value(1)) # leg
            akt_leg.append(query.value(2)) # set
            akt_leg.append(query.value(3)) # winner
            legek.append(akt_leg)
        # Egy listában meg van az adott torna összes lejátszott leg-je
        # Kinullázzuk az eredményeket, mert a lekérdezés az összeset tudja lekérni, nem csak a legfrissebbet!!!
        for x in range(self.csoportok_szama):
            for y in range(self.sorok_szama):
                for z in range(self.sorok_szama):
                    self.eredmenyek[x][y][z]._set_leg1(0)
                    self.eredmenyek[x][y][z]._set_leg2(0)
        # Először összegezzük mindenhol a nyert legeket
        for k in legek:
            for x in range(self.csoportok_szama):
                for y in range(self.sorok_szama):
                    for z in range(self.sorok_szama):
                        if self.eredmenyek[x][y][z]._get_p1_id() == k[1] and self.eredmenyek[x][y][z]._get_p2_id() == k[2]:
                            if self.eredmenyek[x][y][z]._get_p1_id() == k[5]:
                                self.eredmenyek[x][y][z]._set_leg1(self.eredmenyek[x][y][z]._get_leg1() +1)
                                self.eredmenyek[x][y][z].change_leg1_number()
                            else:
                                self.eredmenyek[x][y][z]._set_leg2(self.eredmenyek[x][y][z]._get_leg2() + 1)
                                self.eredmenyek[x][y][z].change_leg2_number()
                        # ellenfél szempontjából:
                        if self.eredmenyek[x][y][z]._get_p1_id() == k[2] and self.eredmenyek[x][y][z]._get_p2_id() == k[1]:
                            if self.eredmenyek[x][y][z]._get_p1_id() == k[5]:
                                self.eredmenyek[x][y][z]._set_leg1(self.eredmenyek[x][y][z]._get_leg1() + 1)
                                self.eredmenyek[x][y][z].change_leg1_number()
                            else:
                                self.eredmenyek[x][y][z]._set_leg2(self.eredmenyek[x][y][z]._get_leg2() + 1)
                                self.eredmenyek[x][y][z].change_leg2_number()
        # Megnézzük, hogy valaki megnyerte-e. Ha igen akkor a nyerésért/vereségért járó pontot rögzítjük
        for x in range(self.csoportok_szama):
            for y in range(self.sorok_szama):
                for z in range(self.sorok_szama):
                    if self.eredmenyek[x][y][z]._get_leg1() == self.nyereshez_kell:
                        self.eredmenyek[x][y][z]._set_pontszam(int(self.pont_gyozelem))
                        self.eredmenyek[x][y][z].update_osszes_pont()
                    if self.eredmenyek[x][y][z]._get_leg2() == self.nyereshez_kell:
                        self.eredmenyek[x][y][z]._set_pontszam(int(self.pont_vereseg))
                        self.eredmenyek[x][y][z].update_osszes_pont()

class SzumWidget(QWidget):
    def __init__(self, parent=None):
        super(SzumWidget, self).__init__(parent)
        self.setFixedSize(50, 50)
        self._ertek = 0
        self._p_id = 0
        self.painter = QPainter()

    def _set_p_id(self, number):
        self._p_id = number
        self.update()

    def _set_ertek(self, number):
        self._ertek = number
        self.update()

    def _get_p_id(self):
        return self._p_id

    def _get_ertek(self):
        return self._ertek

    def paintEvent(self, event):
        self.painter.begin(self)
        pen0 = QPen()
        pen0.setWidth(0)
        pen_def = self.painter.pen()
        pen_white = QPen(QColor(255, 255, 255))
        pen_black = QPen(QColor(0, 0, 0))
        pen_blue = QPen(QColor(0, 0, 255))
        pen_red = QPen(QColor(255, 0, 0))
        brush_black = QBrush(QColor(0, 0, 0))
        brush_ready = QBrush(QColor(170, 255, 255))
        brush_csak1 = QBrush(QColor(255, 255, 255))

        self.painter.setBrush(brush_csak1)
        self.painter.setPen(pen0)
        self.painter.drawRect(0, 0, 49, 49)
        self.painter.setPen(pen_black)
        self.painter.drawText(25, 30, str(self._ertek))

        self.painter.end()


class EredmenyWidget(QWidget):
    def __init__(self, parent=None):
        super(EredmenyWidget, self).__init__(parent)
        self.parent = parent
        self.setFixedSize(50, 50)
        self._player1_id = 0
        self._player2_id = 0
        self._csoport_number = 0
        self._csoport_sor = 0
        self._csoport_oszlop = 0
        self._leg1 = 0
        self._leg2 = 0
        self._pontszam = -1
        self.painter = QPainter()

    def update_osszes_pont(self):
        self.parent.szum_eredmenyek[self._csoport_number][3][self._csoport_sor]._set_ertek(0)
        for oszlop in range(self.parent.sorok_szama):
            self.parent.szum_eredmenyek[self._csoport_number][3][self._csoport_sor]._set_ertek(
                self.parent.szum_eredmenyek[self._csoport_number][3][self._csoport_sor]._get_ertek() +
                self.parent.eredmenyek[self._csoport_number][self._csoport_sor][oszlop]._get_pontszam())

    def change_leg1_number(self):
        self.parent.szum_eredmenyek[self._csoport_number][0][self._csoport_sor]._set_ertek(0)
        for oszlop in range(self.parent.sorok_szama):
            self.parent.szum_eredmenyek[self._csoport_number][0][self._csoport_sor]._set_ertek(
                self.parent.szum_eredmenyek[self._csoport_number][0][self._csoport_sor]._get_ertek() +
                self.parent.eredmenyek[self._csoport_number][self._csoport_sor][oszlop]._leg1)
        self.change_legs_dif()

    def change_leg2_number(self):
        self.parent.szum_eredmenyek[self._csoport_number][1][self._csoport_sor]._set_ertek(0)
        for oszlop in range(self.parent.sorok_szama):
            self.parent.szum_eredmenyek[self._csoport_number][1][self._csoport_sor]._set_ertek(
                self.parent.szum_eredmenyek[self._csoport_number][1][self._csoport_sor]._get_ertek() +
                self.parent.eredmenyek[self._csoport_number][self._csoport_sor][oszlop]._leg2)
        self.change_legs_dif()

    def change_legs_dif(self):
        self.parent.szum_eredmenyek[self._csoport_number][2][self._csoport_sor]._set_ertek(
            self.parent.szum_eredmenyek[self._csoport_number][0][self._csoport_sor]._get_ertek() -
            self.parent.szum_eredmenyek[self._csoport_number][1][self._csoport_sor]._get_ertek())

    def _set_csoport_number(self, number):
        self._csoport_number = number
        self.update()

    def _set_csoport_sor(self, number):
        self._csoport_sor = number
        self.update()

    def _set_csoport_oszlop(self, number):
        self._csoport_oszlop = number

    def _set_p1_id(self, number):
        self._player1_id = number
        self.update()

    def _set_p2_id(self, number):
        self._player2_id = number
        self.update()

    def _set_pontszam(self, number):
        self._pontszam = number
        self.update()

    def _set_leg1(self, number):
        self._leg1 = number
        self.update()

    def _set_leg2(self, number):
        self._leg2 = number
        self.update()

    def _get_leg1(self):
        return self._leg1

    def _get_leg2(self):
        return self._leg2

    def _get_p1_id(self):
        return self._player1_id

    def _get_p2_id(self):
        return self._player2_id

    def _get_pontszam(self):
        # Ha még nem játszották le 0-t ad vissza, egyébként a konkrét pontot
        if self._pontszam < 0:
            return 0
        else:
            return self._pontszam

    def paintEvent(self, event):
        self.painter.begin(self)
        pen0 = QPen()
        pen0.setWidth(0)
        pen_def = self.painter.pen()
        pen_white = QPen(QColor(255, 255, 255))
        pen_black = QPen(QColor(0, 0, 0))
        pen_blue = QPen(QColor(0, 0, 255))
        pen_red = QPen(QColor(255, 0, 0))
        brush_black = QBrush(QColor(0, 0, 0))
        brush_ready = QBrush(QColor(170, 255, 255))
        brush_csak1 = QBrush(QColor(255, 255, 255))
        brush_end = QBrush(QColor(200, 255, 150))

        if self._player1_id == self._player2_id:
            self.painter.setBrush(brush_black)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            self.painter.setPen(pen_red)
            # self.painter.drawText(2, 10, str(self._player1_id))
            # self.painter.drawText(2, 20, str(self._player2_id))
            # self.painter.drawText(20, 35, "X")
        elif self._player1_id == 0 or self._player2_id == 0:
            self.painter.setBrush(brush_csak1)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            self.painter.setPen(pen_blue)
            self.painter.drawText(2, 10, str(self._player1_id))
            self.painter.drawText(2, 20, str(self._player2_id))
            self.painter.drawText(25, 30, "X")
        else:
            if self._pontszam >= 0:
                self.painter.setBrush(brush_end)
            else:
                self.painter.setBrush(brush_ready)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            self.painter.setPen(pen_black)
            self.painter.drawText(12, 20, str(self._leg1))
            self.painter.drawText(23, 20, " : ")
            self.painter.drawText(33, 20, str(self._leg2))
            if self._pontszam >= 0:
                self.painter.drawText(21, 32, str(self._pontszam))
        self.painter.end()


class GroupMemberWidget(QWidget):
    def __init__(self, parent=None):
        super(GroupMemberWidget, self).__init__(parent)
        self.parent = parent
        self.setFixedSize(200, 50)
        self.setAcceptDrops(True)
        self._player_name = ""
        self._player_id = 0
        self._csoport_number = 0
        self._csoport_sor = 0
        self.painter = QPainter()

    def _set_player_id(self, number):
        self._player_id = number
    # todo a beállításnál ez legyen használva
    def _set_csoport_number(self, number):
        self._csoport_number = number

    def _set_csoport_sor(self, number):
        self._csoport_sor = number

    def _set_player_name(self, name):
        self._player_name = name
        self.update()

    def _get_player_id(self):
        return int(self._player_id)

    def _get_csoport_number(self):
        return int(self._csoport_number)

    def _get_csoport_sor(self):
        return int(self._csoport_sor)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(QPen(QColor("blue")))
        self.painter.setBrush(QBrush(QColor("lightgray")))
        pen0 = QPen()
        pen0.setWidth(0)
        pen = self.painter.pen()
        self.painter.setPen(pen0)
        self.painter.drawRect(0, 0, 199, 49)
        self.painter.setPen(pen)
        self.painter.drawText(20, 35, str(self._player_id) + "   " + str(self._csoport_sor + 1) + "    " + self._player_name)
        self.painter.end()

if __name__ == '__main__':
    app = QApplication([])
    win = TornaStatuszWindow()
    win.show()
    app.exec_()