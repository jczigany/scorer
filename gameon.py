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
        self.resize(1000, 800)

        self.params = []
        self.set_layouts()
        # # Fő LAYOUT létrehozása, beállítása
        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        # # Legfelső sor (nevek) Widget max magassággal, hozzárendelve egy LAYOUT, amihez hozzáadjuk a neveket
        # self.nevek_sor = QWidget()
        # self.nevek_sor.setFixedHeight(60)
        # self.nevek_layout = QHBoxLayout()
        # self.nevek_sor.setLayout(self.nevek_layout)
        # A neveket tartalmazó QLabel-ek létrehozása, hozzáadása a neveket tartalmazó layout-hoz
        self.nev1 = QLabel()
        self.nev1.setAlignment(Qt.AlignCenter)
        self.nev1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 35px; font-family: Cuorier New")
        self.nev2 = QLabel()
        self.nev2.setAlignment(Qt.AlignCenter)
        self.nev2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 35px; font-family: Cuorier New")
        self.nevek_layout.addWidget(self.nev1)
        self.nevek_layout.addWidget(self.nev2)
        # # Az info sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        # self.info_sor = QWidget()
        # self.info_sor.setFixedHeight(100)
        # self.info_layout = QHBoxLayout()
        # self.info_sor.setLayout(self.info_layout)
        # # a PONT1 megjelenítéséhez Widget, layout
        # self.score1_widget = QWidget()
        # self.score1_widget.setFixedHeight(100)
        # self.score1_layout = QVBoxLayout()
        # self.score1_widget.setLayout(self.score1_layout)
        # # A PONT1 Widget hozzáadása az info LAYOUT-hoz
        # self.info_layout.addWidget(self.score1_widget)
        # A konkrét pontszámot tartalmazó widget hozzáadása a pont1 widget layout-jához
        self.score1_layout.addWidget(QLabel("PONT1"))
        # # Set1, Leg1 megjelenítéséhez Widget, Layout
        # self.legset1_widget = QWidget()
        # self.legset1_widget.setMaximumHeight(100)
        # self.legset1_layout = QVBoxLayout()
        # self.legset1_widget.setLayout(self.legset1_layout)
        # self.leg1_layout = QHBoxLayout()
        # self.set1_layout = QHBoxLayout()
        # self.legset1_layout.addLayout(self.leg1_layout)
        self.leg1_layout.addWidget(QLabel("Leg:"))
        self.leg1_layout.addWidget(QLabel("11"))
        # self.legset1_layout.addLayout(self.set1_layout)
        self.set1_layout.addWidget(QLabel("Set:"))
        self.set1_layout.addWidget(QLabel("3"))
        # self.info_layout.addWidget(self.legset1_widget)
        # # Set2, Leg2 megjelenítéséhez Widget, Layout
        # self.legset2_widget = QWidget()
        # self.legset2_widget.setMaximumHeight(100)
        # self.legset2_layout = QVBoxLayout()
        # self.legset2_widget.setLayout(self.legset2_layout)
        # self.leg2_layout = QHBoxLayout()
        # self.set2_layout = QHBoxLayout()
        # self.legset2_layout.addLayout(self.leg2_layout)
        self.leg2_layout.addWidget(QLabel("Leg:"))
        self.leg2_layout.addWidget(QLabel("11"))
        # self.legset2_layout.addLayout(self.set2_layout)
        self.set2_layout.addWidget(QLabel("Set:"))
        self.set2_layout.addWidget(QLabel("3"))
        # self.info_layout.addWidget(self.legset2_widget)


        # # a PONT2 megjelenítéséhez Widget, layout
        # self.score2_widget = QWidget()
        # self.score2_widget.setFixedHeight(100)
        # self.score2_layout = QVBoxLayout()
        # self.score2_widget.setLayout(self.score2_layout)
        # # A PONT1 Widget hozzáadása az info LAYOUT-hoz
        # self.info_layout.addWidget(self.score2_widget)
        # A konkrét pontszámot tartalmazó widget hozzáadása a pont1 widget layout-jához
        self.score2_layout.addWidget(QLabel("PONT2"))

        # # A konténer-widget-ek ( nevek, info-sor, ....) hozzáadása a fő LAYOUT-hoz
        # self.layout.addWidget(self.nevek_sor)
        # self.layout.addWidget(self.info_sor)
        #
        # # self.gomb1 = QPushButton("Gombocska")
        # # self.layout.addWidget(self.gomb1)
        # self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.layout.addItem(self.space)

    def set_layouts(self):
        # Fő LAYOUT létrehozása, beállítása
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Legfelső sor (nevek) Widget max magassággal, hozzárendelve egy LAYOUT, amihez hozzáadjuk a neveket
        self.nevek_sor = QWidget()
        self.nevek_sor.setFixedHeight(60)
        self.nevek_layout = QHBoxLayout()
        self.nevek_sor.setLayout(self.nevek_layout)
        # Az info sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.info_sor = QWidget()
        self.info_sor.setFixedHeight(100)
        self.info_layout = QHBoxLayout()
        self.info_sor.setLayout(self.info_layout)
        # a PONT1 megjelenítéséhez Widget, layout
        self.score1_widget = QWidget()
        self.score1_widget.setFixedHeight(100)
        self.score1_layout = QVBoxLayout()
        self.score1_widget.setLayout(self.score1_layout)
        # A PONT1 Widget hozzáadása az info LAYOUT-hoz
        self.info_layout.addWidget(self.score1_widget)
        # Set1, Leg1 megjelenítéséhez Widget, Layout
        self.legset1_widget = QWidget()
        self.legset1_widget.setMaximumHeight(100)
        self.legset1_layout = QVBoxLayout()
        self.legset1_widget.setLayout(self.legset1_layout)
        self.leg1_layout = QHBoxLayout()
        self.set1_layout = QHBoxLayout()
        self.legset1_layout.addLayout(self.leg1_layout)
        self.legset1_layout.addLayout(self.set1_layout)
        self.info_layout.addWidget(self.legset1_widget)
        # Set2, Leg2 megjelenítéséhez Widget, Layout
        self.legset2_widget = QWidget()
        self.legset2_widget.setMaximumHeight(100)
        self.legset2_layout = QVBoxLayout()
        self.legset2_widget.setLayout(self.legset2_layout)
        self.leg2_layout = QHBoxLayout()
        self.set2_layout = QHBoxLayout()
        self.legset2_layout.addLayout(self.leg2_layout)
        self.legset2_layout.addLayout(self.set2_layout)
        self.info_layout.addWidget(self.legset2_widget)
        # a PONT2 megjelenítéséhez Widget, layout
        self.score2_widget = QWidget()
        self.score2_widget.setFixedHeight(100)
        self.score2_layout = QVBoxLayout()
        self.score2_widget.setLayout(self.score2_layout)
        # A PONT1 Widget hozzáadása az info LAYOUT-hoz
        self.info_layout.addWidget(self.score2_widget)
        # A konténer-widget-ek ( nevek, info-sor, ....) hozzáadása a fő LAYOUT-hoz
        self.layout.addWidget(self.nevek_sor)
        self.layout.addWidget(self.info_sor)

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