from PySide2.QtWidgets import QSpacerItem, QWidget, QMessageBox, QDialog, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy
from PySide2.QtCore import *
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel


db = QSqlDatabase.addDatabase('QMYSQL')
db.setHostName('localhost')
db.setDatabaseName('cida')
db.setUserName('cida')
db.setPassword('cida')

if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)


class GameWindowDialog(QDialog):
    def __init__(self, parent = None):
        super(GameWindowDialog, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.resize(800, 600)

        self.params = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info_sor = QWidget()
        self.info_sor.setFixedHeight(100)
        self.info_layout = QHBoxLayout()
        self.info_sor.setLayout(self.info_layout)

        self.layout.addWidget(self.info_sor)
        self.nev1 = QLineEdit()
        self.nev2 = QLineEdit()
        self.info_layout.addWidget(QLabel("Játékos 1:"))
        self.info_layout.addWidget(self.nev1)
        self.info_layout.addWidget(QLabel("Játékos 2:"))
        self.info_layout.addWidget(self.nev2)

        self.gomb1 = QPushButton("Gombocska")
        self.layout.addWidget(self.gomb1)
        self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.space)

    def refresh(self):
        self.nev1.setText(self.params[0])
        self.nev2.setText(self.params[1])


if __name__ == '__main__':
    app = QApplication([])
    win = GameWindowDialog()
    win.show()
    app.exec_()