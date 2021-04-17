from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QDrag
from PySide2.QtCore import Qt, QMimeData, QDataStream, QIODevice, QByteArray

cegek = ["Videoton", "RF-IT", "Create Value", "Bernstein", "Datalogic", "DIME"]

class CsoportTabla(QWidget):
    def __init__(self, parent=None):
        super(CsoportTabla, self).__init__(parent)
        self.setWindowTitle("Drag&Drop CustomWidget-el")
        self.create_widgets()
        self.set_layout()
        self.resize(400, 300)

    def create_widgets(self):
        self.resztvevok = resztvevokLista()
        self.csoporttag1 = GroupMemberWidget()
        self.csoporttag2 = GroupMemberWidget()
        self.csoporttag3 = GroupMemberWidget()
        self.csoporttag4 = GroupMemberWidget()
        self.csoporttag5 = GroupMemberWidget()
        self.csoporttag6 = GroupMemberWidget()

    def set_layout(self):
        main_layout = QHBoxLayout()
        widgets_layout = QVBoxLayout()
        widgets_layout.addWidget(self.csoporttag1)
        widgets_layout.addWidget(self.csoporttag2)
        widgets_layout.addWidget(self.csoporttag3)
        widgets_layout.addWidget(self.csoporttag4)
        widgets_layout.addWidget(self.csoporttag5)
        widgets_layout.addWidget(self.csoporttag6)
        lista_layout = QVBoxLayout()
        lista_layout.addWidget(self.resztvevok)
        main_layout.addLayout(widgets_layout)
        main_layout.addLayout(lista_layout)
        self.setLayout(main_layout)

class resztvevokLista(QListWidget):
    def __init__(self):
        super(resztvevokLista, self).__init__()
        self.setMaximumWidth(200)
        self.setMaximumHeight(300)
        for i in cegek:
            self.addItem(i)
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
            # icon = QIcon()
            # stream >> icon
            item = QListWidgetItem(text, self)
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
        self.resize(200, 50)
        self.setAcceptDrops(True)
        self.felirat = "Kezdés"
        self.painter = QPainter()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(QPen(QColor("blue")))
        self.painter.setBrush(QBrush(QColor("lightgray")))
        self.painter.drawRect(0, 0, 200, 50)
        self.painter.drawText(20, 35, self.felirat)
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
            self.felirat = stream.readQString()
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
        stream.writeQString(self.felirat)
        mimedata = QMimeData()
        mimedata.setData("application/x-lista-item", data)
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            self.felirat = "Kezdés"
            self.update()

app = QApplication([])
win = CsoportTabla()
win.show()
app.exec_()
