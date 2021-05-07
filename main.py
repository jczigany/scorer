from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide2.QtCore import *
from PySide2.QtGui import QImage, QPainter
import os, sys
from menus import create_menus
from gamesettings2 import GameSettingsDialog
from gameon import GameWindowDialog
from net_settings import NetworkSettingsDialog
from match_stat import MatchStatWindow
from select_match import SelectMatchWindow
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from database import create_tables

db = QSqlDatabase.addDatabase('QMYSQL')
db.setHostName('192.168.68.22')
db.setDatabaseName('cida')
db.setUserName('cida')
db.setPassword('cida')
# db = QSqlDatabase.addDatabase('QSQLITE')
# db.setDatabaseName('scorer.db3')

if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)
else:
    create_tables(db)
    # todo: Ezt ki kell egészíteni minden táblára


class AppWindows(QMainWindow):
    def __init__(self):
        super(AppWindows, self).__init__()
        self.setWindowTitle("Darts Scorer powered by Jcigi")
        self.resize(1000,1000)
        self.widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

        self.background_image = QImage("images/gdc_logo_uj.png")
        self.image_rect = QRect()
        # A menus.py definiálja a menüpontokat
        create_menus(self)

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawWidget(painter)
        painter.end()

    def drawWidget(self, painter):
        rect = self.rect()
        hatter = self.background_image.scaled(QSize(rect.width(), rect.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_rect.setRect(rect.x(), rect.y(), hatter.width(), hatter.height())
        self.image_rect.moveCenter(rect.center())
        painter.setOpacity(0.05)
        painter.drawImage(self.image_rect, QImage(hatter))


    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def new_game(self):
        self.new_game_window = GameWindowDialog(self)
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
    app.exec_()
