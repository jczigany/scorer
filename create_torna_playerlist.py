from PySide2.QtWidgets import QListWidget, QListWidgetItem, QDialogButtonBox, QMessageBox, QDialog, \
    QApplication, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlRelation
from PySide2.QtCore import *
import configparser, os, sys

# db = QSqlDatabase.addDatabase('QMYSQL')
# db.setHostName('192.168.68.22')
# db.setDatabaseName('cida')
# db.setUserName('cida')
# db.setPassword('cida')
# # db = QSqlDatabase.addDatabase('QSQLITE')
# # db.setDatabaseName('scorer.db3')
config = configparser.ConfigParser()
# # Ha a progiból indul, nem kell majd
# if not db.open():
#     QMessageBox.critical(
#         None,
#         "App Name - Error!",
#         "Database Error: %s" % db.lastError().text(),
#     )
#     sys.exit(1)


class SelectPlayersWindow(QDialog):
    def __init__(self, parent = None):
        super(SelectPlayersWindow, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setWindowTitle("Torna résztvevők")
        self.resize(520, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.read_config()

        self.create_torna_selection()

        self.nevek_layout = QHBoxLayout()
        self.layout.addLayout(self.nevek_layout)
        self.show_saved_players()
        self.show_torna_players()

        self.gomb_nev_layout = QVBoxLayout()
        self.nevek_layout.addLayout(self.gomb_nev_layout)
        self.show_current_players()

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.clicked.connect(self.buttonbox_click)
        self.layout.addWidget(self.buttonbox)

    def create_torna_selection(self):
        self.tournaments = QComboBox()
        self.tournaments.setModelColumn(0)
        self.tournaments.currentIndexChanged.connect(self.torna_valasztas)
        self.layout.addWidget(self.tournaments)
        self.load_torna()

    def load_torna(self):
        torna = QSqlQueryModel()
        query = QSqlQuery("select * from torna_settings where aktiv=2")
        torna.setQuery(query)
        if torna.record(0).value(0):
            for i in range(torna.rowCount()):
                self.tournaments.addItem(torna.record(i).value(1), torna.record(i).value(0)) # a value(0) a torna_id
        else:
            print("Nincs aktív torna")

    def show_saved_players(self):
        self.saved_players = QListWidget()
        self.saved_players.setFixedHeight(500)
        self.saved_players.setFixedWidth(150)
        self.saved_players.setSortingEnabled(True)
        self.saved_players.itemDoubleClicked.connect(self.add_resztvevo)
        self.load_saved_players()
        self.nevek_layout.addWidget(self.saved_players)

    def show_torna_players(self):
        self.torna_players = QListWidget()
        self.torna_players.setFixedHeight(500)
        self.torna_players.setFixedWidth(150)
        self.torna_players.setSortingEnabled(True)
        self.torna_players.itemDoubleClicked.connect(self.add_resztvevo)
        self.load_torna_players()
        self.nevek_layout.addWidget(self.torna_players)

    def load_saved_players(self):
        players = QSqlQueryModel()
        players_query = QSqlQuery("select * from players where aktiv=1")
        players.setQuery(players_query)
        self.saved_players.clear()
        for i in range(players.rowCount()):
            item = QListWidgetItem(players.record(i).value(1))
            item.setData(Qt.UserRole, players.record(i).value(0))
            self.saved_players.addItem(item)

    def load_torna_players(self):
        players = QSqlQueryModel()
        players_query = QSqlQuery("select * from torna_resztvevok where 1 group by player_id, player_name")
        players.setQuery(players_query)
        self.torna_players.clear()
        for i in range(players.rowCount()):
            item = QListWidgetItem(players.record(i).value(1))
            item.setData(Qt.UserRole, players.record(i).value(0))
            self.torna_players.addItem(item)

    def add_resztvevo(self, item):
        new_item = QListWidgetItem(item)
        new_item.setData(Qt.UserRole, item.data(Qt.UserRole))
        self.current_players.addItem(new_item)
        query = QSqlQuery(
            f"insert into torna_resztvevok (player_id, player_name, torna_id) values ({new_item.data(Qt.UserRole)}, '{new_item.text()}', {self.torna_id})")
        query.exec_()

    def show_current_players(self):
        query = QSqlQuery("select max(player_id) from torna_resztvevok")
        query.exec_()
        while query.next():
            self.first_new_id = int(query.value(0)) + 1
        print(self.first_new_id)
        self.add_new = QPushButton("Új")
        self.add_new.clicked.connect(self.uj_ember)
        self.current_players = QListWidget()
        self.current_players.setFixedHeight(470)
        self.current_players.setFixedWidth(150)
        self.current_players.setSortingEnabled(True)
        self.gomb_nev_layout.addWidget(self.add_new)
        self.current_players.itemDoubleClicked.connect(self.remove_resztvevo)
        self.gomb_nev_layout.addWidget(self.current_players)

    def uj_ember(self):
        ujember, ok = QInputDialog.getText(self, "Új versenyző",
                                           '<html style="font-size: 15px;">Írd be a versenyző nevét!</html>')
        if ok and len(ujember):
            item = QListWidgetItem(ujember)
            item.setData(Qt.UserRole, self.first_new_id)
            self.current_players.addItem(item)
            self.first_new_id += 1

            query = QSqlQuery(f"insert into torna_resztvevok (player_id, player_name, torna_id) values ({item.data(Qt.UserRole)}, '{item.text()}', {self.torna_id})")
            query.exec_()

    def remove_resztvevo(self, item):
        self.current_players.takeItem(self.current_players.row(self.current_players.selectedItems()[0]))
        # print(item.data(Qt.UserRole), item.text())
        query = QSqlQuery(f"delete from torna_resztvevok where player_id={item.data(Qt.UserRole)} and torna_id={self.torna_id}")
        query.exec_()

    def torna_valasztas(self, i):
        self.torna_id = self.tournaments.itemData(i)
        players = QSqlQueryModel()
        players_query = QSqlQuery(f"select * from torna_resztvevok where torna_id={self.torna_id}")
        players.setQuery(players_query)
        self.current_players.clear()
        for i in range(players.rowCount()):
            item = QListWidgetItem(players.record(i).value(1))
            item.setData(Qt.UserRole, players.record(i).value(0))
            self.current_players.addItem(item)

    def buttonbox_click(self, b):
        if b.text() == "OK":
            self.accept()
        elif b.text() == "Cancel":
            self.reject()

    def accept(self):
        # for i in range(self.current_players.count()):
        #     item = self.current_players.item(i)
        #     print(self.torna_id, item.data(Qt.UserRole), item.text()) # itt vannak a beszúrandó adatok
        super().accept()
        # INSERT INTO `torna_resztvevok` (`player_id`, `player_name`, `torna_id`)
        # VALUES ('1111', 'teszt_user2', '8892') ON DUPLICATE KEY UPDATE player_name='teszt_user2';
    def read_config(self):
        if os.path.exists('config.ini'):
            # Van config.ini, ki kell értékelni
            config.read('config.ini')
            self.station_id = config['DEFAULT'].get('station id')
            self.secret = config['DEFAULT'].get('secret key')
            # todo módosítani kell a torna_match táblát, hogy tartalmazza a tabla mellett a hozzá tartozó secret-et is
        else:
            # Nincs config.ini, alapértékekkel inicializálni
            msg = QMessageBox(self)
            msg.setStyleSheet("fonz-size: 20px")
            msg.setWindowTitle("Hiányzó beállítás file!")
            msg.setText(
                '<html style="font-size: 14px; color: red">Nem tudtam beolvasni a konfigurációt!<br></html>' + '<html style="font-size: 16px">Kérem módosítsa a beállításokat!</html>')
            msg.exec_()
            sys.exit(1)

if __name__ == '__main__':
    app = QApplication([])
    win = SelectPlayersWindow()
    win.show()
    app.exec_()