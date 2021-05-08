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

# csoportok_szama = 2
# sorok_szama = 5
# torna_id = 8888
# variant = "501"
# sets = 1
# legsperset = 5
# csoport_tabla = [6, 5, 5, 6]



torna_id = 8888
# csoportok_szama = 0  # todo torna_settings-ből lekérni a 'csoportok_szama' ahol a torna_id a megadott
# sorok_szama = 0 # todo torna_settings-ből lekérni a 'fo_per_csoport' ahol a torna_id a megadott
csoport_tabla = [6, 5] # todo ez sem a settings-ben, sem a torna_tablakban nincs rögzítve(a torna_match tartalmazza, ott viszont a csoport száma nincs




class TornaStatuszWindow(QDialog):
    def __init__(self, parent=None):
        super(TornaStatuszWindow, self).__init__(parent)
        self.setWindowTitle("Torna állása")
        self.get_params()
        self.create_widgets()
        self.set_layout()

    def get_params(self):
        query = QSqlQuery(f"select csoportok_szama, fo_per_csoport from torna_settings where torna_id={torna_id}")
        query.exec_()
        query.first()
        self.csoportok_szama = query.value(0)
        self.sorok_szama = query.value(1)
        print(self.csoportok_szama)
        print(self.sorok_szama)
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
                    self.eredmeny_oszlop[x]._set_csoport_sor(x)
                    self.eredmeny_oszlop[x]._set_csoport_oszlop(j)
                    self.eredmeny_oszlop[x]._set_p1_id(self.tablak[i][j])
                    self.eredmeny_oszlop[x]._set_p2_id(self.tablak[i][x])

                self.csoport_eredmeny_matrix.append(self.eredmeny_oszlop)
            self.eredmenyek.append(self.csoport_eredmeny_matrix)

    def set_layout(self):
        main_layout = QHBoxLayout()
        groups = QWidget()
        groups.setFixedWidth((self.sorok_szama * 50) + 200 )
        widgets_layout = QVBoxLayout()
        # widgets_layout
        groups.setLayout(widgets_layout)

        for n in range(self.csoportok_szama): # csoportok száma
            locals()['csoport_layout' + str(n)] = QGridLayout() # Létrehozzuk az adott sorszámú csoport layout-ját
            locals()['csoport_layout' + str(n)].setContentsMargins(0, 0, 0, 0)
            locals()['csoport_layout' + str(n)].setHorizontalSpacing(0)
            locals()['csoport_layout' + str(n)].setVerticalSpacing(0)
            widgets_layout.addLayout(locals()['csoport_layout' + str(n)]) # Hozzáadjuk a a layout-ot a widget_layout-hoz
            for i in range(len(self.csoportok[n])):  # len(self.csoportok[n]) : csoporton belüli sorok száma
            # Végigmegyünk a sorokon   :  i: sorok száma, n: csoport száma
                # a layout 1. oszlopát feltöltjük a tömbben tárolt custom widget-ekkel
                locals()['csoport_layout' + str(n)].addWidget(self.csoportok[n][i], i + 1, 0)
                # todo itt ugyanígy kell hozzáadni az eredményösszesítő widgeteket
                # Itt töltjük fel az eredmény-widget-eket (tombben tárolva, mint a GroupMemberWidget-ek)
                # eredmenyek[x, y, z] x: csoport, y: oszlop, z: sor
                for x in range(len(self.csoportok[n])): # Ez lesz az oszlop(max = sorok száma) x: oszlop száma
                    locals()['csoport_layout' + str(n)].addWidget(self.eredmenyek[n][i][x], i + 1, x + 1)

            # widgets_layout.addWidget(EredmenyWidget())
            locals()['csoport_layout' + str(n)].addWidget(QLabel("Csoport_" + str(n + 1)), 0, 0)

        scroll = QScrollArea()
        scroll.setWidget(groups)
        # scroll.setWidgetResizable(True)
        scroll.setFixedWidth((self.sorok_szama * 50) + 220)
        scroll.setFixedHeight(600)

        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

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
        self.painter = QPainter()

    def _set_csoport_number(self, number):
        self._csoport_number = number
        self.update()

    def _set_csoport_sor(self, number):
        self._csoport_sor = number
        self.update()

    def _set_p1_id(self, number):
        self._player1_id = number
        self.update()

    def _set_p2_id(self, number):
        self._player2_id = number
        self.update()

    def _get_p1_id(self):
        return self._player1_id

    def _get_p2_id(self):
        return self._player2_id

    def _set_csoport_oszlop(self, number):
        self._csoport_oszlop = number

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

        if self._player1_id == self._player2_id:
            self.painter.setBrush(brush_black)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            self.painter.setPen(pen_red)
            self.painter.drawText(2, 10, str(self._player1_id))
            self.painter.drawText(2, 20, str(self._player2_id))
            self.painter.drawText(20, 35, "X")
        elif self._player1_id == 0 or self._player2_id == 0:
            self.painter.setBrush(brush_csak1)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            self.painter.setPen(pen_blue)
            self.painter.drawText(2, 10, str(self._player1_id))
            self.painter.drawText(2, 20, str(self._player2_id))
            self.painter.drawText(20, 35, "X")
        else:
            self.painter.setBrush(brush_ready)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            self.painter.setPen(pen_black)
            self.painter.drawText(2, 10, str(self._player1_id))
            self.painter.drawText(2, 20, str(self._player2_id))
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
        self.painter.drawText(20, 35, str(self._csoport_number) + ":" + str(self._csoport_sor) + ":" + self._player_name)
        self.painter.end()


app = QApplication([])
win = TornaStatuszWindow()
win.show()
app.exec_()