from PySide6.QtWidgets import QMainWindow, QWidget, QDialog, QApplication, QLayout, QVBoxLayout, QGridLayout, \
    QPushButton, QLabel, QMessageBox, QHBoxLayout, QLineEdit
from PySide6.QtCore import *
from PySide6.QtGui import QImage, QPainter, QPen, QBrush, QColor, QPixmap, QDrag, QFont
import os, sys
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from database import create_tables


class MeccsLapWindow(QMainWindow):
    def __init__(self):
        super(MeccsLapWindow, self).__init__()
        self.setWindowTitle("Csoport-levezető powered by Jcigi")
        self.resize(1000, 1000)
        self.db_config()
        self.widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        self.background_image = QImage("images/gdc_logo_uj.png")
        self.image_rect = QRect()
        # todo: itt még tömb, majd db-ből kell szedni
        players = ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7"]
        datas = ["Won", "Lost", "Diff", "Points", "Rank"]
        sorokszama = len(players)
        oszlopokszama = len(players)
        eredmenyek = [[0] * oszlopokszama for i in range(sorokszama)]

        self.racs = QGridLayout()
        self.racs.setSpacing(0)
        self.racs.setSizeConstraint(QLayout.SetFixedSize)
        self.main_layout.addLayout(self.racs)

        # mérkőzés eredmények: sor+1 és oszlop+1-től
        for s in range(sorokszama):
            for o in range(oszlopokszama):
                self.ered = EredmenyWidget()
                self.ered._set_l1(0)
                self.ered._set_l2(0)
                self.ered._set_poz(s, o)

                eredmenyek[s][o] = self.ered
                self.racs.addWidget(self.ered, s + 1, o + 1)

        # Játékosnevek bal oldalon
        for y in range(len(players)):
            gomb = QPushButton(players[y])
            self.racs.addWidget(gomb, y + 1, 0)
            gomb.setStyleSheet("background-color: gray")
            gomb.setFixedWidth(150)
            gomb.setFixedHeight(50)

        # Játékosnevek felső sorban
        for x in range(len(players)):
            gomb = QPushButton(players[x])
            self.racs.addWidget(gomb, 0, x + 1)
            gomb.setStyleSheet("background-color: gray")
            gomb.setFixedWidth(50)
            gomb.setFixedHeight(150)

        # Szum mezők felsősorban nevek után
        for xx in range(len(datas)):
            gomb = QPushButton(datas[xx])
            self.racs.addWidget(gomb, 0, x + xx + 2)
            gomb.setStyleSheet("background-color: gray")
            gomb.setFixedWidth(50)
            gomb.setFixedHeight(150)

        # össszegzések: 1 sortól, 8. oszloptól
        for s in range(sorokszama):
            for o in range(8,13):
                self.szum = SzumWidget()
                self.racs.addWidget(self.szum, s + 1, o)

    def db_config(self):
        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName('37.46.67.53')
        self.db.setDatabaseName('cida')
        self.db.setUserName('cida')
        self.db.setPassword('cida')
        if not self.db.open():
            QMessageBox.critical(
                None,
                "App Name - Error!",
                "Database Error: %s" % self.db.lastError().text(),
            )
            sys.exit(1)

    def eredmegnyom(self, sor, oszlop):
        print("Sor: " + str(sor) + " - Oszlop: " + str(oszlop))

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawWidget(painter)
        painter.end()

    def drawWidget(self, painter):
        rect = self.rect()
        hatter = self.background_image.scaled(QSize(rect.width(), rect.height()), Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
        self.image_rect.setRect(rect.x(), rect.y(), hatter.width(), hatter.height())
        self.image_rect.moveCenter(rect.center())
        painter.setOpacity(0.05)
        painter.drawImage(self.image_rect, QImage(hatter))


class EredmenyWidget(QWidget):
    def __init__(self, parent=None):
        super(EredmenyWidget, self).__init__(parent)
        self.painter = QPainter()
        self.sor = 0
        self.oszlop = 0
        self.l1 = 0
        self.l2 = 0
        self.p = 0
        self.felso = ""
        self.also = ""

    def _set_poz(self, _sor, _oszlop):
        self.sor = _sor
        self.oszlop = _oszlop
        self.update()

    def _set_l1(self, _l1):
        self.l1 = _l1
        self._set_felso()

    def _set_l2(self, _l2):
        self.l2 = _l2
        self._set_felso()

    def _set_felso(self):
        self.felso = str(self.l1) + " : " + str(self.l2)
        if (self.l1 == 0) and (self.l2 == 0):
            self.also = str(0)
        else:
            if self.l1 > self.l2:
                self.also = str(2)
            elif self.l1 < self.l2:
                self.also = str(0)
            else:
                self.also = str(1)
        self.update()

    def eredmeny_dialog(self):
        self.dlg = QDialog(self)
        layout = QVBoxLayout()
        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle("Eredmény")
        cimke1 = QLabel("J1:")
        self.e1 = QLineEdit()
        self.e1.setText(str(self.sor))
        cimke2 = QLabel("J2:")
        sor1 = QHBoxLayout()
        self.e2 = QLineEdit()
        self.e2.setText(str(self.oszlop))
        sor1.addWidget(cimke1)
        sor1.addWidget(self.e1)
        sor2 = QHBoxLayout()
        sor2.addWidget(cimke2)
        sor2.addWidget(self.e2)
        layout.addLayout(sor1)
        layout.addLayout(sor2)

    def mouseDoubleClickEvent(self, event):
        print("dupla klikk")
        self.eredmeny_dialog()
        self.dlg.exec()
        #self.setDisabled(True)

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
        if self.sor != self.oszlop:
            self.painter.setBrush(brush_csak1)
        else:
            self.painter.setBrush(brush_black)
        self.painter.setPen(pen0)
        self.painter.drawRect(0, 0, 49, 49)
        self.painter.setPen(pen_black)
        self.painter.drawText(10, 20, self.felso)
        self.painter.drawText(22, 40, self.also)
        self.painter.end()


class SzumWidget(QWidget):
    def __init__(self, parent=None):
        super(SzumWidget, self).__init__(parent)
        self.csakdupla = False
        self.setFixedSize(50, 50)
        # self._ertek = 0
        # self._p_id = 0
        self.painter = QPainter()
        #self.clicked.connect(self.megnyomtad)

    def mouseDoubleClickEvent(self, event):
        print("dupla klikk")
        self.csakdupla = False

    def mousePressEvent(self, event):
        if self.csakdupla:
            pass
        else:
            print("Klikk")
            self.csakdupla = True

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
        self.painter.drawText(10, 30, str("szum"))
        self.painter.end()

if __name__ == '__main__':
    app = QApplication([])
    win = MeccsLapWindow()
    win.show()
    app.exec()