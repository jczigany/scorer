from PySide2.QtWidgets import QSpacerItem, QWidget, QMessageBox, QDialog, QLabel, QLineEdit, \
    QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy, QTextEdit
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
        # A neveket tartalmazó QLabel-ek létrehozása, hozzáadása a neveket tartalmazó layout-hoz
        self.nev1 = QLabel()
        self.nev1.setAlignment(Qt.AlignCenter)
        self.nev1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 35px; font-family: Cuorier New")
        self.nev2 = QLabel()
        self.nev2.setAlignment(Qt.AlignCenter)
        self.nev2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 35px; font-family: Cuorier New")
        self.nevek_layout.addWidget(self.nev1)
        self.nevek_layout.addWidget(self.nev2)
        # A konkrét pontszámot tartalmazó widget hozzáadása a pont1 widget layout-jához
        self.score1_layout.addWidget(QLabel("PONT1"))
        # Set1, Leg1 megjelenítéséhez Widget, Layout
        self.leg1_layout.addWidget(QLabel("Leg:"))
        self.leg1_layout.addWidget(QLabel("11"))
        self.set1_layout.addWidget(QLabel("Set:"))
        self.set1_layout.addWidget(QLabel("3"))
        # Set2, Leg2 megjelenítéséhez Widget, Layout
        self.leg2_layout.addWidget(QLabel("Leg:"))
        self.leg2_layout.addWidget(QLabel("11"))
        self.set2_layout.addWidget(QLabel("Set:"))
        self.set2_layout.addWidget(QLabel("3"))
        # A konkrét pontszámot tartalmazó widget hozzáadása a pont2 widget layout-jához
        self.score2_layout.addWidget(QLabel("PONT2"))
        # A CHEKOUT1-ET tartalmazó Widget hozzáadása a checkout1 widget layout-jához
        self.check1 = QLabel("Check-Out 1")
        self.check1.setAlignment(Qt.AlignCenter)
        self.check1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 30px")
        self.check1_layout.addWidget(self.check1)
        # A CHEKOUT2-ET tartalmazó Widget hozzáadása a checkout2 widget layout-jához
        self.check2 = QLabel("Check-Out 2")
        self.check2.setAlignment(Qt.AlignCenter)
        self.check2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 30px")
        self.check2_layout.addWidget(self.check2)
        # Az aktuális pontszámot tartalmazó Widget hozzáadása a current widget layout-jához
        self.current = QLabel("180")
        self.current.setAlignment(Qt.AlignCenter)
        self.current.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 50px")
        self.current_layout.addWidget(self.current)
        # A statisztika1-et tartalmazo widget hozzáadása a stat1 layout-hoz
        self.stat1 = QLabel("Stat1")
        self.stat1.setAlignment(Qt.AlignCenter)
        self.stat1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 50px")
        self.stat1_layout.addWidget(self.stat1)
        # A statisztika2-et tartalmazo widget hozzáadása a stat2 layout-hoz
        self.stat2 = QLabel("Stat2")
        self.stat2.setAlignment(Qt.AlignCenter)
        self.stat2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 50px")
        self.stat2_layout.addWidget(self.stat2)
        # A körök1-et tartalmazo widget hozzáadása a korok1 layout-hoz
        self.kor1 = QLabel("KÖR1")
        self.kor1.setAlignment(Qt.AlignCenter)
        self.kor1.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 50px")
        self.round1_layout.addWidget(self.kor1)
        # A körök2-et tartalmazo widget hozzáadása a korok2 layout-hoz
        self.kor2 = QLabel("KÖR2")
        self.kor2.setAlignment(Qt.AlignCenter)
        self.kor2.setStyleSheet("background-color: cornflowerblue; border-radius: 5px; font-size: 50px")
        self.round2_layout.addWidget(self.kor2)

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
        # Az checkout sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.checkout_sor = QWidget()
        self.checkout_sor.setFixedHeight(100)
        self.checkout_layout = QHBoxLayout()
        self.checkout_sor.setLayout(self.checkout_layout)
        # A státusz sor. Widget max magassággal, hozzárendelve egy LAYOUT,
        self.statusz_sor = QWidget()
        self.statusz_sor.setFixedHeight(500)
        self.statusz_layout = QHBoxLayout()
        self.statusz_sor.setLayout(self.statusz_layout)
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
        # A PONT2 Widget hozzáadása az info LAYOUT-hoz
        self.info_layout.addWidget(self.score2_widget)
        # a CHEKOUT1 megjelenítéséhez Widget, layout
        self.check1_widget = QWidget()
        self.check1_widget.setFixedHeight(100)
        self.check1_layout = QVBoxLayout()
        self.check1_widget.setLayout(self.check1_layout)
        # A PONT2 Widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.check1_widget, 42)
        # A dobott pont megjelenítéséhez Widget, layout
        self.current_widget = QWidget()
        self.current_widget.setFixedHeight(100)
        self.current_layout = QVBoxLayout()
        self.current_widget.setLayout(self.current_layout)
        # Az aktuális pont widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.current_widget, 16)
        # a CHEKOUT2 megjelenítéséhez Widget, layout
        self.check2_widget = QWidget()
        self.check2_widget.setFixedHeight(100)
        self.check2_layout = QVBoxLayout()
        self.check2_widget.setLayout(self.check2_layout)
        # A PONT2 Widget hozzáadása a checkout layout-hoz
        self.checkout_layout.addWidget(self.check2_widget, 42)
        # a STAT1 megjelenítéséhez Widget, layout
        self.stat1_widget = QWidget()
        self.stat1_widget.setFixedHeight(500)
        self.stat1_layout = QVBoxLayout()
        self.stat1_widget.setLayout(self.stat1_layout)
        # A stat1 Widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.stat1_widget, 20)
        #A körök1 megjelenítéséhez widget, layout
        self.round1_widget = QWidget()
        self.round1_widget.setFixedHeight(500)
        self.round1_layout = QVBoxLayout()
        self.round1_widget.setLayout(self.round1_layout)
        # A round1 widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.round1_widget, 30)
        # A körök2 megjelenítéséhez widget, layout
        self.round2_widget = QWidget()
        self.round2_widget.setFixedHeight(500)
        self.round2_layout = QVBoxLayout()
        self.round2_widget.setLayout(self.round2_layout)
        # A round1 widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.round2_widget, 30)
        # a STAT2 megjelenítéséhez Widget, layout
        self.stat2_widget = QWidget()
        self.stat2_widget.setFixedHeight(500)
        self.stat2_layout = QVBoxLayout()
        self.stat2_widget.setLayout(self.stat2_layout)
        # A stat2 Widget hozzáadása a statusz layout-hoz
        self.statusz_layout.addWidget(self.stat2_widget, 20)

        # A konténer-widget-ek ( nevek, info-sor, ....) hozzáadása a fő LAYOUT-hoz
        self.layout.addWidget(self.nevek_sor)
        self.layout.addWidget(self.info_sor)
        self.layout.addWidget(self.checkout_sor)
        self.layout.addWidget(self.statusz_sor)
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