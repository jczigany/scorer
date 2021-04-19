from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QListWidget, QListWidgetItem, QPushButton, QDialog, QLabel
from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QDrag
from PySide2.QtCore import Qt, QMimeData, QDataStream, QIODevice, QByteArray
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel

db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('scorer.db3')
# Ha a progiból indul, nem kell majd
if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)

cegek = [
    [1015, "Videoton"],
    [1016, "RF-IT"],
    [1017, "Create Value"],
    [1018, "Bernstein"],
    [1019, "Datalogic"],
    [1020, "DIME"],
    [1021, "eSpell"],
    [1022, "NetIng"],
    [1023, "Infobiz"],
    [1024, "Info-Mágus"],
    [1025, "Eurocert"],
    [1026, "Domusch"],
    [1027, "Hajdú"],
    [1028, "Brand Made"]
]
csoportok_szama = 2
sorok_szama = 4
torna_id = 8888
variant = "501"
sets = 1
legsperset = 5
csoport_tabla = [6, 5, 5, 6]

class CsoportTabla(QDialog):
    def __init__(self, parent=None):
        super(CsoportTabla, self).__init__(parent)
        self.setWindowTitle("Drag&Drop CustomWidget-el")
        self.create_widgets()
        self.set_layout()
        self.resize(1000, 400)

    def create_widgets(self):
        self.resztvevok = resztvevokLista()

        # GroupMemberWidget-ek
        self.csoportok = []
        for i in range(csoportok_szama): # Csoportok száma
            self.csoportoszlop = []
            for j in range(sorok_szama): # fő/csoport
                self.csoportoszlop.append(GroupMemberWidget(self))
                self.csoportoszlop[j]._set_csoport_number(i)
                self.csoportoszlop[j]._set_csoport_sor(j)
            self.csoportok.append(self.csoportoszlop)

        # EredmenyWidget-ek
        self.eredmenyek = []
        for i in range(csoportok_szama):
            self.csoport_eredmeny_matrix = []
            for j in range(sorok_szama): # ami egyenlő az oszlopok számával!!!
                self.eredmeny_oszlop = []
                for x in range(sorok_szama):
                    self.eredmeny_oszlop.append(EredmenyWidget(self))
                    self.eredmeny_oszlop[x]._set_csoport_number(i)
                    self.eredmeny_oszlop[x]._set_csoport_sor(x)
                    self.eredmeny_oszlop[x]._set_csoport_oszlop(j)

                self.csoport_eredmeny_matrix.append(self.eredmeny_oszlop)
            self.eredmenyek.append(self.csoport_eredmeny_matrix)

        # Gombok
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_records)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_all_record)

    def set_layout(self):
        main_layout = QHBoxLayout()
        groups = QWidget()
        widgets_layout = QVBoxLayout()
        groups.setLayout(widgets_layout)

        for n in range(csoportok_szama): # csoportok száma
            locals()['csoport_layout' + str(n)] = QGridLayout() # Létrehozzuk az adott sorszámú csoport layout-ját
            widgets_layout.addLayout(locals()['csoport_layout' + str(n)]) # Hozzáadjuk a a layout-ot a widget_layout-hoz
            for i in range(len(self.csoportok[n])):  # len(self.csoportok[n]) : csoporton belüli sorok száma
            # Végigmegyünk a sorokon   :  i: sorok száma, n: csoport száma
                # a layout 1. oszlopát feltöltjük a tömbben tárolt custom widget-ekkel
                locals()['csoport_layout' + str(n)].addWidget(self.csoportok[n][i], i + 1, 0)
                # Itt töltjük fel az eredmény-widget-eket (tombben tárolva, mint a GroupMemberWidget-ek)
                # eredmenyek[x, y, z] x: csoport, y: oszlop, z: sor
                for x in range(len(self.csoportok[n])): # Ez lesz az oszlop(max = sorok száma) x: oszlop száma
                    locals()['csoport_layout' + str(n)].addWidget(self.eredmenyek[n][i][x], i + 1, x + 1)

            # widgets_layout.addWidget(EredmenyWidget())
            locals()['csoport_layout' + str(n)].addWidget(QLabel("Csoport_" + str(n + 1)), 0, 0)

        lista_layout = QVBoxLayout()
        lista_layout.addWidget(self.resztvevok)
        lista_layout.addWidget(self.generate_button)
        lista_layout.addWidget(self.clear_button)

        scroll = QScrollArea()
        scroll.setWidget(groups)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)

        main_layout.addWidget(scroll)
        main_layout.addLayout(lista_layout)
        self.setLayout(main_layout)

    def clear_all_record(self):
        print("Rekordok törlése")
        # model = QSqlQueryModel()
        query = QSqlQuery(f"delete from torna_match where torna_id={torna_id}")
        query.exec_()
        # model.setQuery(query)

    def generate_records(self):
        print("Rekordok generálása")
        match_rekords = []
        for cs in range(csoportok_szama):
            for sor in range(sorok_szama):
                for oszlop in range(sor + 1, sorok_szama):
                    # print(self.eredmenyek[cs][sor][oszlop]._get_p1_id(), ":", self.eredmenyek[cs][sor][oszlop]._get_p2_id())
                    if self.eredmenyek[cs][sor][oszlop]._get_p1_id() != 0 and self.eredmenyek[cs][sor][oszlop]._get_p2_id() != 0:
                        match_id = (10000 * torna_id) + (100 * int(self.eredmenyek[cs][sor][oszlop]._get_p1_id())) + int(self.eredmenyek[cs][sor][oszlop]._get_p2_id()) # todo generálni kell az adatok alapján
                        match_rekord = []
                        match_rekord.append(torna_id)
                        match_rekord.append(match_id)
                        match_rekord.append(self.eredmenyek[cs][sor][oszlop]._get_p1_id())
                        match_rekord.append(self.eredmenyek[cs][sor][oszlop]._get_p2_id())
                        match_rekord.append(variant)
                        match_rekord.append(sets)
                        match_rekord.append(legsperset)
                        match_rekord.append(csoport_tabla[cs])
                        match_rekords.append(match_rekord)
        for x in range(len(match_rekords)):
            print(match_rekords[x])

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
        pen_white = QPen(QColor(255, 255, 255))
        pen_black = QPen(QColor(0, 0, 0))
        pen_blue = QPen(QColor(0, 0, 255))
        pen_red = QPen(QColor(255, 0, 0))
        brush_black = QBrush(QColor(0, 0, 0))
        brush_ready = QBrush(QColor(170, 255, 255))
        brush_csak1 = QBrush(QColor(255, 255, 255))

        if self._player1_id == self._player2_id:
            self.painter.setPen(pen_red)
            self.painter.setBrush(brush_black)
            self.painter.drawRect(0, 0, 50, 50)
            self.painter.drawText(15, 20, str(self._player1_id) + " : " + str(self._player2_id))
            self.painter.drawText(20, 35, "X")
        elif self._player1_id == 0 or self._player2_id == 0:
            self.painter.setPen(pen_blue)
            self.painter.setBrush(brush_csak1)
            self.painter.drawRect(0, 0, 50, 50)
            self.painter.drawText(15, 20, str(self._player1_id) + " : " + str(self._player2_id))
            self.painter.drawText(20, 35, "X")
        else:
            self.painter.setPen(pen_black)
            self.painter.setBrush(brush_ready)
            self.painter.drawRect(0, 0, 50, 50)
            self.painter.drawText(15, 20, str(self._player1_id) + " : " + str(self._player2_id))
        self.painter.end()


class resztvevokLista(QListWidget):
    def __init__(self):
        super(resztvevokLista, self).__init__()
        self.setMaximumWidth(200)
        self.setMaximumHeight(300)
        for i in cegek:
            item = QListWidgetItem(i[1])
            item.setData(1, i[0])
            self.addItem(item)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

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

    def _set_csoport_number(self, number):
        self._csoport_number = number

    def _set_csoport_sor(self, number):
        self._csoport_sor = number

    def _get_csoport_number(self):
        return int(self._csoport_number)

    def _get_csoport_sor(self):
        return int(self._csoport_sor)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(QPen(QColor("blue")))
        self.painter.setBrush(QBrush(QColor("lightgray")))
        self.painter.drawRect(0, 0, 200, 50)
        self.painter.drawText(20, 35, str(self._csoport_number) + ":" + str(self._csoport_sor) + ":" + self._player_name)
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
            for i in range(sorok_szama):
                self.parent.eredmenyek[self._csoport_number][self._csoport_sor][i]._set_p1_id(self._player_id)
                self.parent.eredmenyek[self._csoport_number][i][self._csoport_sor]._set_p2_id(self._player_id)
            print("id: ", self._player_id, "csoport: ", self._get_csoport_number(), "sor: ", self._get_csoport_sor())
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
            for i in range(sorok_szama):
                self.parent.eredmenyek[self._csoport_number][self._csoport_sor][i]._set_p1_id(0)
                self.parent.eredmenyek[self._csoport_number][i][self._csoport_sor]._set_p2_id(0)
            self.update()

app = QApplication([])
win = CsoportTabla()
win.show()
app.exec_()
