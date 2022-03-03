from PySide6.QtWidgets import QListWidget, QDialogButtonBox, QMessageBox, QDialog, QApplication, QComboBox, QVBoxLayout
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlRelation
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


class SelectMatchWindow(QDialog):
    def __init__(self, parent = None):
        super(SelectMatchWindow, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setWindowTitle("Mérkőzés választása")
        self.resize(600, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.read_config()
        self.tournaments = QComboBox()
        self.tournaments.setModelColumn(0)
        self.tournaments.currentIndexChanged.connect(self.torna_valasztas)
        self.layout.addWidget(self.tournaments)
        self.merkozesek = QListWidget()
        self.merkozesek.setFixedHeight(300)
        self.merkozesek.setFixedWidth(500)
        self.merkozesek.itemDoubleClicked.connect(self.start_game)
        self.merkozesek.itemSelectionChanged.connect(self.start_game)
        self.layout.addWidget(self.merkozesek)

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.clicked.connect(self.buttonbox_click)
        self.layout.addWidget(self.buttonbox)

        self.load_torna()

    def load_torna(self):
        torna = QSqlQueryModel()
        query = QSqlQuery("select * from torna_settings where aktiv=1")
        torna.setQuery(query)
        if torna.record(0).value(0):
            for i in range(torna.rowCount()):
                self.tournaments.addItem(torna.record(i).value(1), torna.record(i).value(0)) # a value(0) a torna_id
        else:
            print("Nincs aktív torna")

    def torna_valasztas(self, i):
        print(self.tournaments.itemData(i))
        # matches = QSqlRelationalTableModel()
        # matches.setTable("torna_match")
        # matches.setFilter(f'a.torna_id=8889 and a.player1_id=c.player_id and a.player2_id=d.player_id and c.torna_id=a.torna_id and d.torna_id=a.torna_id and a.torna_id=b.torna_id')
        # matches.setFilter(f'torna_name = "{self.tournaments.currentText()}" and torna_resztvevok.torna_id=torna_settings.torna_id and station_id = "{self.station_id}"')
        # matches.setRelation(0, QSqlRelation("torna_settings", "torna_id", "torna_name"))
        # matches.setRelation(2, QSqlRelation("torna_resztvevok", "player_id", "player_name"))
        # matches.setRelation(3, QSqlRelation("torna_resztvevok", "player_id", "player_name"))
        # matches.setRelation(7, QSqlRelation("reged_station", "id", "station_id"))
        # matches.select()
        # print(matches)
        # self.merkozesek.clear()
        # for i in  range(matches.rowCount()):
        #     self.merkozesek.addItem(matches.record(i).value(0) + "\t" +
        #                             str(matches.record(i).value(1)) + "\t" +
        #                             matches.record(i).value(2) + "\t" +
        #                             matches.record(i).value(3) + "\t" +
        #                             matches.record(i).value(4) + "\t" +
        #                             str(matches.record(i).value(5))+ "\t" +
        #                             str(matches.record(i).value(6)))
        matches = QSqlQueryModel()
        # todo itt még nincs táblához kötve a lekérés

        matches_query = QSqlQuery(f'SELECT a.match_id,  b.torna_name, c.player_name as nev1, \
        d.player_name as nev2, a.variant, a.sets, a.legsperset FROM `torna_match` a, torna_settings b, torna_resztvevok c, \
        torna_resztvevok d WHERE a.torna_id={self.tournaments.itemData(i)} and a.player1_id=c.player_id and a.player2_id=d.player_id \
        and c.torna_id=a.torna_id and d.torna_id=a.torna_id and a.torna_id=b.torna_id and a.tabla={self.station_id} and a.match_status<2')
        matches.setQuery(matches_query)
        self.merkozesek.clear()
        print(matches.record(2))
        for i in range(matches.rowCount()):
            self.merkozesek.addItem(str(matches.record(i).value(0)) + "\t" +
                                    matches.record(i).value(1) + "\t" +
                                    matches.record(i).value(2) + "\t" +
                                    matches.record(i).value(3) + "\t" +
                                    matches.record(i).value(4) + "\t" +
                                    str(matches.record(i).value(5)) + "\t" +
                                    str(matches.record(i).value(6))
            )

    def buttonbox_click(self, b):
        if b.text() == "OK":
            self.accept()
        elif b.text() == "Cancel":
            self.reject()

    def read_config(self):
        if os.path.exists('config.ini'):
            # Van config.ini, ki kell értékelni
            config.read('config.ini')
            self.station_id = config['DEFAULT'].get('station id')
            self.secret = config['DEFAULT'].get('secret key')
            # print(self.station_id)
            # print(self.secret)
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

    def start_game(self):
        para = self.merkozesek.currentItem().text().rsplit("\t")
        p1_model = QSqlQueryModel()
        p1_query = QSqlQuery(f"select player_id from torna_resztvevok where player_name='{para[2]}'")
        p1_model.setQuery(p1_query)
        p2_model = QSqlQueryModel()
        p2_query = QSqlQuery(f"select player_id from torna_resztvevok where player_name='{para[3]}'")
        p2_model.setQuery(p2_query)

        params = []
        params.append(para[2])
        params.append(para[3])
        params.append(int(para[0]))
        self.match_id = int(para[0])
        params.append(int(p1_model.record(0).value(0)))
        params.append(int(p2_model.record(0).value(0)))
        params.append(para[4])
        params.append(int(para[6]))
        params.append(int(para[5]))
        params.append(0)    # hc1
        params.append(0)    # hc2
        params.append(0)    #bets_of...
        self.parent.new_game_window.params = params
        self.parent.new_game_window.refresh()

    def accept(self):
        query = QSqlQuery(f"update torna_match set match_status=1 where match_id={self.match_id}")
        query.exec_()
        #self.match_id
        super().accept()

    def reject(self):
        self.parent.new_game_window.close()
        super().reject()

if __name__ == '__main__':
    app = QApplication([])
    win = SelectMatchWindow()
    win.show()
    app.exec_()