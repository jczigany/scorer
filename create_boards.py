from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QListWidget, \
    QListWidgetItem, QPushButton, QDialog, QLabel, QMessageBox, QComboBox, QSpacerItem, QSizePolicy
from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QDrag, QFont
from PySide2.QtCore import Qt, QMimeData, QDataStream, QIODevice, QByteArray
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
import sys

db = QSqlDatabase.addDatabase('QMYSQL')
db.setHostName('192.168.68.22')
db.setDatabaseName('cida')
db.setUserName('cida')
db.setPassword('cida')


# db = QSqlDatabase.addDatabase('QSQLITE')
# db.setDatabaseName('scorer.db3')
# Ha a progiból indul, nem kell majd
if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)

# cegek = [
#     [1015, "Videoton"],
#     [1016, "RF-IT"],
#     [1017, "Create Value"],
#     [1018, "Bernstein"],
#     [1019, "Datalogic"],
#     [1020, "DIME"],
#     [1021, "eSpell"],
#     [1022, "NetIng"],
#     [1023, "Infobiz"],
#     [1024, "Info-Mágus"],
#     [1025, "Eurocert"],
#     [1026, "Domusch"],
#     [1027, "Hajdú"],
#     [1028, "Brand Made"]
# ]
# csoportok_szama = 4
# sorok_szama = 4
# torna_id = 8889
# variant = "501"
# sets = 1
# legsperset = 5
# csoport_tabla = [6, 5, 5, 6]

class CsoportTabla(QDialog):
    def __init__(self, parent=None):
        super(CsoportTabla, self).__init__(parent)
        self.setWindowTitle("Csoportok, ágak összeállítása")
        self.setMinimumHeight(650)
        # self.setMinimumWidth(700)
        # self.resize(800, 650)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.hatter = QVBoxLayout()
        self.setLayout(self.hatter)

        self.create_torna_selection()
        self.hatter.addWidget(self.tournaments)

        self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.hatter.addItem(self.space)
        # self.create_widgets()
        # self.set_layout()

    def create_widgets(self):
        if hasattr(self, 'resztvevok'):
            self.resztvevok.load_data(self.torna_id)
        else:
            self.resztvevok = resztvevokLista(self.torna_id)
            self.resztvevok.load_data(self.torna_id)

        # GroupMemberWidget-ek
        self.csoportok = []
        for i in range(self.csoportok_szama): # Csoportok száma
            self.csoportoszlop = []
            for j in range(self.sorok_szama): # fő/csoport
                self.csoportoszlop.append(GroupMemberWidget(self))
                self.csoportoszlop[j]._set_csoport_number(i)
                self.csoportoszlop[j]._set_csoport_sor(j)
                self.csoportoszlop[j]._set_sorok_szama(self.sorok_szama)
            self.csoportok.append(self.csoportoszlop)

        # EredmenyWidget-ek
        self.eredmenyek = []
        for i in range(self.csoportok_szama):
            self.csoport_eredmeny_matrix = []
            for j in range(self.sorok_szama): # ami egyenlő az oszlopok számával!!!
                self.eredmeny_oszlop = []
                for x in range(self.sorok_szama):
                    self.eredmeny_oszlop.append(EredmenyWidget(self))
                    self.eredmeny_oszlop[x]._set_csoport_number(i)
                    self.eredmeny_oszlop[x]._set_csoport_sor(x)
                    self.eredmeny_oszlop[x]._set_csoport_oszlop(j)

                self.csoport_eredmeny_matrix.append(self.eredmeny_oszlop)
            self.eredmenyek.append(self.csoport_eredmeny_matrix)

        # Gombok
        if hasattr(self, 'generate_button'):
            pass
        else:
            self.generate_button = QPushButton("Generate")
            self.generate_button.clicked.connect(self.generate_match_records)
            # self.clear_button = QPushButton("Clear")
            # self.clear_button.clicked.connect(self.clear_all_torna_match) # todo visszarakni, de ez mindent töröl!!!!

    # def clear_layout(self, lay):
    #     if lay is not None:
    #         while lay.count():
    #             child = lay.takeAt(0)
    #             if child.widget() is not None:
    #                 child.widget().deleteLater()
    #             elif child.layout() is not None:
    #                 self.clear_layout(child.layout())

    def set_layout(self):
        if hasattr(self, 'main_layout'):
            for i in reversed(range(self.main_layout.count())):
                if self.main_layout.itemAt(i).widget() is not None:
                    self.main_layout.itemAt(i).widget().deleteLater()
            for i in reversed(range(self.main_layout.count())):
                if self.main_layout.itemAt(i).layout() is not None:
                    self.main_layout.itemAt(i).layout().deleteLater()
        else:
            self.main_layout = QHBoxLayout()
            self.hatter.addLayout(self.main_layout)

        groups = QWidget()
        groups.setFixedWidth((self.sorok_szama * 50) + 200 )
        widgets_layout = QVBoxLayout()
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
                # Itt töltjük fel az eredmény-widget-eket (tombben tárolva, mint a GroupMemberWidget-ek) eredmenyek[x, y, z] x: csoport, y: oszlop, z: sor
                for x in range(len(self.csoportok[n])): # Ez lesz az oszlop(max = sorok száma) x: oszlop száma
                    locals()['csoport_layout' + str(n)].addWidget(self.eredmenyek[n][i][x], i + 1, x + 1)
            locals()['csoport_layout' + str(n)].addWidget(QLabel("Csoport_" + str(n + 1)), 0, 0)

        lista_layout = QVBoxLayout()
        lista_layout.addWidget(self.resztvevok)
        lista_layout.addWidget(self.generate_button)
        # lista_layout.addWidget(self.clear_button)

        scroll = QScrollArea()
        scroll.setWidget(groups)
        scroll.setFixedWidth((self.sorok_szama * 50) + 220 )
        scroll.setFixedHeight(600)
        scroll.updateGeometry()

        self.main_layout.addWidget(scroll)
        self.main_layout.addLayout(lista_layout)

    def create_torna_selection(self):
        self.tournaments = QComboBox()
        self.tournaments.setMinimumWidth(500)
        self.tournaments.setModelColumn(0)
        self.tournaments.activated.connect(self.torna_valasztas)
        self.load_torna()

    def load_torna(self):
        torna = QSqlQueryModel()
        query = QSqlQuery("select * from torna_settings where aktiv=2")
        torna.setQuery(query)
        if torna.record(0).value(0):
            for i in range(torna.rowCount()):
                self.tournaments.addItem(torna.record(i).value(1), torna.record(i).value(0)) # a value(0) a torna_id

    def torna_valasztas(self, i):
        self.torna_id = self.tournaments.itemData(i)
        torna = QSqlQuery(f"select * from torna_settings where torna_id={self.torna_id}")
        torna.exec_()
        while torna.next():
            self.csoportok_szama = torna.value(3)
            self.sorok_szama = torna.value(4)
            self.variant = torna.value(5)
            self.sets = torna.value(7)
            self.legsperset = torna.value(8)

        self.create_widgets()
        self.set_layout()
        # self.hatter.activate()


    def clear_all_torna_match(self):
        print("Rekordok törlése")
        query = QSqlQuery(f"delete from torna_match where torna_id={torna_id}")
        query.exec_()

    def write_tables(self):
        tabla_rekordok = []
        for cs in range(len(self.csoportok)):
            for sor in range(len(self.csoportok[cs])):
                if self.csoportok[cs][sor]._get_player_id() != 0:
                    tabla_rekord = []
                    tabla_rekord.append(self.torna_id)
                    tabla_rekord.append(self.csoportok[cs][sor]._get_player_id())
                    tabla_rekord.append(self.csoportok[cs][sor]._get_csoport_number())
                    tabla_rekord.append(self.csoportok[cs][sor]._get_csoport_sor())
                    tabla_rekordok.append(tabla_rekord)


        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare(
            """ 
            insert into torna_tablak (
                  torna_id,
                  player_id,
                  csoport_number,
                  csoport_sor
            )
            values (?, ?, ?, ?)
            """
        )
        for x in range(len(tabla_rekordok)):
            for i in range(len(tabla_rekordok[x])):
                insertDataQuery.addBindValue(tabla_rekordok[x][i])
            insertDataQuery.exec_()

        query =QSqlQuery(f"update torna_settings set aktiv=1 where torna_id={self.torna_id}")
        query.exec_()

    def generate_match_records(self):
        match_rekords = []
        csoport_tabla = [6, 5, 4, 3, 2, 1] # todo táblához rendeléshez kell majd
        for cs in range(self.csoportok_szama):
            for sor in range(self.sorok_szama):
                for oszlop in range(sor + 1, self.sorok_szama):
                    if self.eredmenyek[cs][sor][oszlop]._get_p1_id() != 0 and self.eredmenyek[cs][sor][oszlop]._get_p2_id() != 0:
                        match_id = (10000 * self.torna_id) + (100 * int(self.eredmenyek[cs][sor][oszlop]._get_p1_id())) + int(self.eredmenyek[cs][sor][oszlop]._get_p2_id())
                        match_rekord = []
                        match_rekord.append(self.torna_id)
                        match_rekord.append(match_id)
                        match_rekord.append(self.eredmenyek[cs][sor][oszlop]._get_p1_id())
                        match_rekord.append(self.eredmenyek[cs][sor][oszlop]._get_p2_id())
                        match_rekord.append(self.variant)
                        match_rekord.append(self.sets)
                        match_rekord.append(self.legsperset)
                        match_rekord.append(csoport_tabla[cs])
                        match_rekords.append(match_rekord)

        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare(
            """ 
            insert into torna_match (
                  torna_id,
                  match_id,
                  player1_id,
                  player2_id,
                  variant,
                  sets,
                  legsperset,
                  tabla
            )
            values (?, ?, ?, ?, ?, ?, ?, ?)
            """
        )
        for x in range(len(match_rekords)):
            for i in range(len(match_rekords[x])):
                insertDataQuery.addBindValue(match_rekords[x][i])
            insertDataQuery.exec_()

        self.write_tables()

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
            # self.painter.setPen(pen_red)
            # self.painter.drawText(15, 20, str(self._player1_id) + " : " + str(self._player2_id))
            # self.painter.drawText(20, 35, "X")
        elif self._player1_id == 0 or self._player2_id == 0:
            self.painter.setBrush(brush_csak1)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            # self.painter.setPen(pen_blue)
            # self.painter.drawText(15, 20, str(self._player1_id) + " : " + str(self._player2_id))
            # self.painter.drawText(20, 35, "X")
        else:
            self.painter.setBrush(brush_ready)
            self.painter.setPen(pen0)
            self.painter.drawRect(0, 0, 49, 49)
            # self.painter.setPen(pen_black)
            # self.painter.drawText(15, 20, str(self._player1_id) + " : " + str(self._player2_id))
        self.painter.end()


class resztvevokLista(QListWidget):
    def __init__(self, torna_id):
        super(resztvevokLista, self).__init__()
        self.torna_id = torna_id
        # self.setMaximumWidth(200)
        # self.clear()
        self.setFixedWidth(200)
        self.setMaximumHeight(300)
        # self.load_data()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def load_data(self, tornaid):
        self.clear()
        query = QSqlQuery(f"select * from torna_resztvevok where torna_id={tornaid}")
        query.exec_()
        while query.next():
            item = QListWidgetItem(query.value(1))
            item.setData(1, query.value(0))
            self.addItem(item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-lista-item"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-lista-item"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-lista-item"):
            data = event.mimeData().data("application/x-lista-item")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            id = stream.readInt16()
            # icon = QIcon()
            # stream >> icon
            item = QListWidgetItem(text, self)
            item.setData(1, id)
            # item.setIcon(icon)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, dropActions):
        item = self.currentItem()
        # icon = item.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(item.text())
        stream.writeInt16(item.data(1))
        # stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-lista-item", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            self.takeItem(self.row(item))


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

    def _set_sorok_szama(self, number):
        self.sorok_szama = number

    def _set_player_id(self, number):
        self._player_id = number
    # todo a beállításnál ez legyen használva
    def _set_csoport_number(self, number):
        self._csoport_number = number

    def _set_csoport_sor(self, number):
        self._csoport_sor = number

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
        font = QFont("Verdana, 20")
        font.setBold(True)
        self.painter.setFont(font)
        self.painter.setPen(pen)
        self.painter.drawText(5, 30, str(self._csoport_sor + 1))
        self.painter.drawText(20, 30, self._player_name)
        self.painter.end()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-lista-item"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-lista-item"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-lista-item"):
            data = event.mimeData().data("application/x-lista-item")
            stream = QDataStream(data, QIODevice.ReadOnly)
            self._player_name = stream.readQString()
            self._player_id = stream.readInt16() # sor eseten p1, oszlopnál p2
            for i in range(self.sorok_szama):
                self.parent.eredmenyek[self._csoport_number][self._csoport_sor][i]._set_p1_id(self._player_id)
                self.parent.eredmenyek[self._csoport_number][i][self._csoport_sor]._set_p2_id(self._player_id)
            # print("id: ", self._player_id, "csoport: ", self._get_csoport_number(), "sor: ", self._get_csoport_sor())
            # icon = QIcon()
            # stream >> icon
            event.setDropAction(Qt.MoveAction)
            event.accept()
            self.update()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        self.startDrag()
        QWidget.mouseMoveEvent(self, event)

    def startDrag(self):
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(self._player_name)
        stream.writeInt16(self._player_id)
        mimedata = QMimeData()
        mimedata.setData("application/x-lista-item", data)
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            self._player_name = ""
            self._player_id = 0
            for i in range(self.sorok_szama):
                self.parent.eredmenyek[self._csoport_number][self._csoport_sor][i]._set_p1_id(0)
                self.parent.eredmenyek[self._csoport_number][i][self._csoport_sor]._set_p2_id(0)
            self.update()

if __name__ == '__main__':
    app = QApplication([])
    win = CsoportTabla()
    win.show()
    app.exec_()
