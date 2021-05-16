from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide2.QtCore import *
from PySide2.QtGui import QImage, QPainter
import os, sys
from menus import create_menus_org
from torna_settings import TornaSettingsDialog
from show_torna_statusz import TornaStatuszWindow
from create_boards import CsoportTabla
from create_torna_playerlist import SelectPlayersWindow
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from database import create_tables

# db1 = QSqlDatabase.addDatabase('QMYSQL')
# db1.setHostName('192.168.68.22')
# db1.setDatabaseName('cida')
# db1.setUserName('cida')
# db1.setPassword('cida')
#
# db1 = QSqlDatabase.addDatabase('QMYSQL', 'database1')
# db1.setHostName('192.168.68.22')
# db1.setDatabaseName('cida')
# db1.setUserName('cida')
# db1.setPassword('cida')
#
# db2 = QSqlDatabase.addDatabase('QSQLITE', 'database2')
# db2.setDatabaseName('scorer.db3')
#
# db = db1
#
# if not db.open():
#     QMessageBox.critical(
#         None,
#         "App Name - Error!",
#         "Database Error: %s" % db.lastError().text(),
#     )
#     sys.exit(1)
# # else:
# #     create_tables(db)
#

class OrgAppWindows(QMainWindow):
    def __init__(self):
        super(OrgAppWindows, self).__init__()
        self.setWindowTitle("Tournament Organization powered by Jcigi")
        self.resize(1000,1000)
        self.widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

        self.background_image = QImage("images/gdc_logo_uj.png")
        self.image_rect = QRect()
        # A menus.py definiálja a menüpontokat
        create_menus_org(self)

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
    def torna_settings(self):
        self.torna_settings_window = TornaSettingsDialog(self)
        self.torna_settings_window.show()

    @Slot()
    def torna_settings2(self):
        self.torna_settings_window = TornaSettingsDialog(self, 8889) # todo ezt majd az aktív tornák közül kell kiválasztani
        self.torna_settings_window.show()

    @Slot()
    def create_players(self):
        self.select_players_window = SelectPlayersWindow(self)
        self.select_players_window.show()

    @Slot()
    def create_boards(self):
        self.create_boards_window = CsoportTabla(self)
        self.create_boards_window.show()

    @Slot()
    def torna_status(self):
        self.torna_status_window = TornaStatuszWindow(self) # todo ezt majd az aktív tornák közül kell kiválasztani
        self.torna_status_window.show()
        # pass

if __name__ == '__main__':
    app = QApplication([])
    win = OrgAppWindows()
    win.show()
    app.exec_()
