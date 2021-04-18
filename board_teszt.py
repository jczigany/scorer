from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QListWidget, QListWidgetItem, QPushButton, QDialog, QLabel
from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QDrag
from PySide2.QtCore import Qt, QMimeData, QDataStream, QIODevice, QByteArray

cegek = [[1, "Videoton"], [2, "RF-IT"], [3, "Create Value"], [4, "Bernstein"], [5, "Datalogic"], [6, "DIME"]]
csoportok_szama = 4
sorok_szama = 6

class CsoportTabla(QDialog):
    def __init__(self, parent=None):
        super(CsoportTabla, self).__init__(parent)
        self.setWindowTitle("Drag&Drop CustomWidget-el")
        self.create_widgets()
        self.set_layout()
        self.setMinimumWidth(465)

    def create_widgets(self):
        self.csoportok = []
        self.resztvevok = resztvevokLista()
        for i in range(csoportok_szama): # Csoportok száma
            self.csoportsor = []
            for j in range(sorok_szama): # fő/csoport
                self.csoportsor.append(GroupMemberWidget())
                self.csoportsor[j]._set_csoport_number(i)
                self.csoportsor[j]._set_csoport_sor(j)
            self.csoportok.append(self.csoportsor)

    def set_layout(self):
        main_layout = QHBoxLayout()
        groups = QWidget()
        widgets_layout = QVBoxLayout()
        groups.setLayout(widgets_layout)

        for n in range(csoportok_szama): # csoportok száma
            locals()['csoport_layout' + str(n)] = QGridLayout() # Létrehozzuk az adott sorszámú csoport layout-ját
            widgets_layout.addLayout(locals()['csoport_layout' + str(n)]) # Hozzáadjuk a a layout-ot a widget_layout-hoz
            for i in range(len(self.csoportok[n])):  # len(self.csoportok[n]) : csoporton belüli sorok száma
            # Végigmegyünk a sorokon
                # a layout 1. oszlopát feltöltjük a tömbben tárolt custom widget-ekkel
                locals()['csoport_layout' + str(n)].addWidget(self.csoportok[n][i], i + 1, 0)
                # Itt töltjük fel az eredmény-widget-eket (tombben tárolva, mint a GroupMemberWidget-ek)
            # widgets_layout.addWidget(QPushButton())
            locals()['csoport_layout' + str(n)].addWidget(QLabel("Csoport_" + str(n + 1)), 0, 0)

        lista_layout = QVBoxLayout()
        lista_layout.addWidget(self.resztvevok)

        scroll = QScrollArea()
        scroll.setWidget(groups)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(600)

        main_layout.addWidget(scroll)
        main_layout.addLayout(lista_layout)
        self.setLayout(main_layout)

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
    def __init__(self):
        super(GroupMemberWidget, self).__init__()
        self.setFixedSize(200, 50)
        self.setAcceptDrops(True)
        self.hidden_player_name = ""
        self.hidden_player_id = 0
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
        self.painter.drawText(20, 35, str(self._csoport_number) + ":" + str(self._csoport_sor) + ":" + self.hidden_player_name)
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
            self.hidden_player_name = stream.readQString()
            self.hidden_player_id = stream.readInt16()
            print("id: ", self.hidden_player_id, "csoport: ", self._get_csoport_number(), "sor: ", self._get_csoport_sor())
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
        stream.writeQString(self.hidden_player_name)
        stream.writeInt16(self.hidden_player_id)
        mimedata = QMimeData()
        mimedata.setData("application/x-lista-item", data)
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            self.hidden_player_name = ""
            self.update()

app = QApplication([])
win = CsoportTabla()
win.show()
app.exec_()
