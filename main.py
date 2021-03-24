from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide2.QtCore import *
from menus import create_menus
from gamesettings2 import GameSettingsDialog
from gameon import GameWindowDialog
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from database import create_tables

# db = QSqlDatabase.addDatabase('QMYSQL')
# db.setHostName('localhost')
# db.setDatabaseName('cida')
# db.setUserName('cida')
# db.setPassword('cida')
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('scorer.db3')

if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)
else:
    create_tables(db)


class AppWindows(QMainWindow):
    def __init__(self):
        super(AppWindows, self).__init__()
        self.setWindowTitle("Darts Scorer powered by Jcigi")
        self.resize(1100,900)
        widget = QWidget()
        self.main_layout = QVBoxLayout()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        # A menus.py definiálja a menüpontokat
        create_menus(self)

        self.match_layout = QVBoxLayout()
        # self.GameWindow = GameWindowDialog()
        # self.main_layout.addWidget(self.GameWindow)
        self.match_layout.addWidget(QPushButton("megy a mecss"))
        self.cimke = QLabel("Csak felirat")
        # self.GameWindow = GameWindowDialog()
        # self.GameWindow.setWindowTitle("Game On!")
        # self.main_layout.addWidget(self.GameWindow)


    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def new_member(self):
        manage_members_window = ManageMembers(self)
        manage_members_window.show()

    @Slot()
    def new_game(self):
        self.new_game_window = GameWindowDialog(self)
        self.settings_window = GameSettingsDialog(self)
        self.new_game_window.show()
        self.settings_window.show()
        # new_game_window.show()
        # new_settings(self)

    @Slot()
    def settings_slot(self):
        new_settings(self)


if __name__ == '__main__':
    app = QApplication([])
    win = AppWindows()
    win.show()
    app.exec_()
