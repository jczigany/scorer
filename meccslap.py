from PySide6.QtWidgets import QMainWindow, QWidget, QSpacerItem, QApplication, QLayout, QVBoxLayout, QGridLayout, \
    QPushButton, QLabel, QMessageBox
from PySide6.QtCore import *
from PySide6.QtGui import QImage, QPainter
import os, sys
from menus import create_menus_org
from torna_settings import TornaSettingsDialog
from show_torna_statusz import TornaStatuszWindow
from create_boards import CsoportTabla
from create_torna_playerlist import SelectPlayersWindow
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from database import create_tables


class OrgAppWindows(QMainWindow):
    def __init__(self):
        super(OrgAppWindows, self).__init__()
        self.setWindowTitle("Csoport-levezető powered by Jcigi")
        self.resize(1000, 1000)
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

        for s in range(sorokszama):
            for o in range(oszlopokszama):
                self.g = QPushButton("")
                self.g.setStyleSheet("background-color: yellow")
                self.g.setFixedWidth(50)
                self.g.setFixedHeight(50)
                if s == o:
                    szoveg = "X"
                    self.g.setDisabled(True)
                    self.g.setStyleSheet("background-color: black")
                else:
                    szoveg = "s: " + str(s) + "-o: " + str(o)
                self.g.setText(szoveg)
                self.g.clicked.connect(lambda sor=s, oszlop=o: self.eredmegnyom(sor, oszlop))
                eredmenyek[s][o] = self.g
                self.racs.addWidget(self.g, s + 1, o + 1)
        # print(eredmenyek)

        for x in range(len(players)):
            gomb = QPushButton(players[x])
            self.racs.addWidget(gomb, 0, x + 1)
            gomb.setStyleSheet("background-color: gray")
            gomb.setFixedWidth(50)
            gomb.setFixedHeight(150)

        for xx in range(len(datas)):
            gomb = QPushButton(datas[xx])
            self.racs.addWidget(gomb, 0, x + xx + 1)
            gomb.setStyleSheet("background-color: gray")
            gomb.setFixedWidth(50)
            gomb.setFixedHeight(150)

        # self.racs.addWidget(QSpacerItem(), 0, x + xx +1)

        for y in range(len(players)):
            gomb = QPushButton(players[y])
            self.racs.addWidget(gomb, y + 1, 0)
            gomb.setStyleSheet("background-color: gray")
            gomb.setFixedWidth(150)
            gomb.setFixedHeight(50)

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

    # @Slot()
    # def exit_app(self):
    #     QApplication.quit()
    #
    # @Slot()
    # def torna_settings(self):
    #     self.torna_settings_window = TornaSettingsDialog(self, self.db)
    #     self.torna_settings_window.show()
    #
    # @Slot()
    # def torna_settings2(self):
    #     self.torna_settings_window = TornaSettingsDialog(self, self.db, 0) # todo ezt majd az aktív tornák közül kell kiválasztani
    #     self.torna_settings_window.show()
    #
    # @Slot()
    # def create_players(self):
    #     self.select_players_window = SelectPlayersWindow(self)
    #     self.select_players_window.show()
    #
    # @Slot()
    # def create_boards(self):
    #     self.create_boards_window = CsoportTabla(self)
    #     self.create_boards_window.show()
    #
    # @Slot()
    # def torna_status(self):
    #     self.torna_status_window = TornaStatuszWindow(self)
    #     self.torna_status_window.show()


if __name__ == '__main__':
    app = QApplication([])
    win = OrgAppWindows()
    win.show()
    app.exec()
