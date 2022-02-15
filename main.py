"""!
Kliens-program dokumentációja
Az adott táblákhoz kerülő kliens program
Alaphelyzetben offline módban is tud működni sqlite db-vel
Képes MySql-t használni, így központilag vannak a játékosok, eredmények rögzítve
Full kliens, így a versenyszervezésben mint végpont szerepel
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QMessageBox
from PySide6.QtCore import *
from PySide6.QtGui import QImage, QPainter
# import os, sys
from menus import create_menus
from gamesettings2 import GameSettingsDialog
from gameon import GameWindowDialog
from net_settings import NetworkSettingsDialog
from match_stat import MatchStatWindow
from select_match import SelectMatchWindow
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
# from database import create_tables

# db = QSqlDatabase.addDatabase('QMYSQL')
# db.setHostName('192.168.68.22')
# db.setDatabaseName('cida')
# db.setUserName('cida')
# db.setPassword('cida')
# # db = QSqlDatabase.addDatabase('QSQLITE')
# # db.setDatabaseName('scorer.db3')
#
# if not db.open():
#     QMessageBox.critical(
#         None,
#         "App Name - Error!",
#         "Database Error: %s" % db.lastError().text(),
#     )
#     sys.exit(1)
# else:
#     create_tables(db)
#     # todo: Ezt ki kell egészíteni minden táblára


class AppWindows(QMainWindow):
    """!
    Az alkalmazás főablaka. Menükön keresztül (és billentyű-kombinációkkal) lehet navigálni.
    A játék, a beállítások, statisztikák... új ablakban jelennek meg.
    Az alapbeállításokon túl, csak a menük generálása történik.
    A háttér beállítás miatt a paintEvent re-definiálva
    """
    def __init__(self):
        """
        Fejléc, méret, és a centralWidget definiálva
        """
        super(AppWindows, self).__init__()
        self.setWindowTitle("Darts Scorer powered by Jcigi")
        self.resize(400,400)
        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName('192.168.68.6')
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
        ## Itt jobb helyen van, mint a drawWidget-ben, ezt csak 1-szer csinálja meg, nem minden újrarajzolásnál
        self.background_image = QImage("images/gdc_logo_uj.png")
        self.image_rect = QRect()
        ## A menus.py definiálja a menüpontokat
        create_menus(self)

    def paintEvent(self, e):
        """!
        csak a drawWidget metódust hívja, az csinál mindent
        :param e: paintEvent
        :return:
        """
        painter = QPainter()
        painter.begin(self)
        self.drawWidget(painter)
        painter.end()

    def drawWidget(self, painter):
        """!
        Betölti a háttér-képet, átméretezi az ablak méretére, létrehozza, majd középre igazítja a képnek a "vásznat"
        végül elhalványítva kirajzolja a hátteret
        :param painter:
        :return:
        """
        rect = self.rect()
        hatter = self.background_image.scaled(QSize(rect.width(), rect.height()), \
                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_rect.setRect(rect.x(), rect.y(), hatter.width(), hatter.height())
        self.image_rect.moveCenter(rect.center())
        painter.setOpacity(0.05)
        painter.drawImage(self.image_rect, QImage(hatter))


    @Slot()
    def exit_app(self):
        """!
        Kilépés az alkalmazásból
        :return:
        """
        QApplication.quit()

    @Slot()
    def new_game(self):
        """!
        Új játék kezdése. A jétkablak és a beállításablak egyidejű létrehozása, megjelenítése.
        A settings ablak átadja a beállított értékeket a játékablaknak.
        Ha megszakítjuk, akkor a játékablak is bezáródik
        :return:
        """
        ## Ablak a áték levezetéséhez.  A GameWindowDialog() osztály példányosítása
        self.new_game_window = GameWindowDialog(self)
        ## Ablak az új játék beállításaihoz.  A GameSettingsDialog() osztály példányosítása
        self.settings_window = GameSettingsDialog(self)
        self.new_game_window.show()
        self.settings_window.show()

    @Slot()
    def network_settings(self):
        self.network_settings_window = NetworkSettingsDialog(self)
        self.network_settings_window.show()

    @Slot()
    def match_history(self):
        self.match_history_window = MatchStatWindow(self)
        self.match_history_window.show()

    @Slot()
    def select_torna(self):
        self.new_game_window = GameWindowDialog(self, place="network")
        self.select_merkozes_window = SelectMatchWindow(self)
        self.new_game_window.show()
        self.select_merkozes_window.show()


if __name__ == '__main__':
    app = QApplication([])
    win = AppWindows()
    win.show()
    app.exec()
