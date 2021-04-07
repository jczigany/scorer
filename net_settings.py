from PySide2.QtWidgets import QSpacerItem, QSizePolicy, QMessageBox, QGridLayout, QDialog, QDialogButtonBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QRadioButton, QSpinBox, QCompleter
from PySide2.QtCore import *
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
import socket, configparser, os, secrets

db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('scorer.db3')
config = configparser.ConfigParser()
#Ez nem kell majd, ha a mainwindow-ból hívom meg
if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class NetworkSettingsDialog(QDialog):
    def __init__(self, parent = None):
        super(NetworkSettingsDialog, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setWindowTitle("Hálózati beállítások")
        self.resize(400, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        adatok = QGridLayout()
        self.layout.addLayout(adatok)

        self.ip = QLineEdit()
        self.token = QLineEdit()
        self.station = QLineEdit()

        self.is_exist_config()
        self.check_config()

        adatok.addWidget(QLabel("IP cím: "), 0, 0)
        # self.ip.setText(get_ip_address())
        self.ip.setDisabled(True)
        adatok.addWidget(self.ip, 0, 1)

        adatok.addWidget(QLabel("Token: "), 1, 0)
        self.token.setDisabled(True)
        adatok.addWidget(self.token, 1, 1)
        adatok.addWidget(QLabel("Állomás azonosító: "), 2, 0)

        self.station.setDisabled(True)
        adatok.addWidget(self.station, 2, 1)
        self.space = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.space)

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.addButton("Módosít", QDialogButtonBox.ActionRole)
        self.buttonbox.button(QDialogButtonBox.Ok).setText('Mentés')
        self.buttonbox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.buttonbox.button(QDialogButtonBox.Cancel).setText('Mégsem')
        self.buttonbox.clicked.connect(self.buttonbox_click)
        self.layout.addWidget(self.buttonbox)

    def is_exist_config(self):
        ip_fizikai = get_ip_address()

        if os.path.exists('config.ini'):
            # Van config.ini, ki kell értékelni
            config.read('config.ini')

            station_id = config['DEFAULT'].get('station id')
            if (station_id is None) or len(station_id) < 4:
                msg = QMessageBox()
                msg.setStyleSheet("fonz-size: 20px")
                msg.setWindowTitle("Hibás állomás név!")
                msg.setText(
                    '<html style="font-size: 14px; color: red">Nem megfelelő állomás-azonosító!<br></html>' + '<html style="font-size: 16px">Kérem módosítsa a beállításokat!</html')
                msg.exec_()
                station = secrets.token_hex(8)
                config.set('DEFAULT', 'station id', station)
                self.station.setText(station)
            # else:
            #     self.station.setText(station_id)

            ip_config = config['DEFAULT'].get('station ip')
            if ip_fizikai != ip_config:
                msg = QMessageBox()
                msg.setStyleSheet("fonz-size: 20px")
                msg.setWindowTitle("Hibás beállítás!")
                msg.setText(
                    '<html style="font-size: 14px; color: red">A fizikai IP cím eltér a konfigurációtól!<br></html>' + '<html style="font-size: 16px">Kérem módosítsa a beállításokat!</html')
                msg.exec_()
                self.ip.setText(ip_fizikai)
                config.set('DEFAULT', 'station ip', ip_fizikai)

            secret = config['DEFAULT'].get('secret key')
            if  (secret is None) or len(secret) != 32:
                newsecret = secrets.token_hex(16)
                config.set('DEFAULT', 'secret key', newsecret)
                self.token.setText(newsecret)

            with open('config.ini', 'w') as configfile:
                config.write(configfile)

        else:
            # Nincs config.ini, alapértékekkel inicializálni
            msg = QMessageBox()
            msg.setStyleSheet("fonz-size: 20px")
            msg.setWindowTitle("Hiányzó beállítás file!")
            msg.setText(
                '<html style="font-size: 14px; color: red">Nem tudtam beolvasni a konfigurációt!<br></html>' + '<html style="font-size: 16px">Kérem módosítsa a beállításokat!</html')
            msg.exec_()
            kulcs = secrets.token_hex(16)
            station = secrets.token_hex(8)
            self.token.setText(kulcs)
            self.ip.setText(ip_fizikai)
            self.station.setText(station)
            config.set('DEFAULT', 'secret key', kulcs)
            config.set('DEFAULT', 'station ip', ip_fizikai)
            config.set('DEFAULT', 'station id', secrets.token_hex(8))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

    def check_config(self):
        ip_config = config['DEFAULT'].get('station ip')
        station_id = config['DEFAULT'].get('station id')
        secret = config['DEFAULT'].get('secret key')
        self.ip.setText(ip_config)
        self.station.setText(station_id)
        self.token.setText(secret)
        # todo Ellenőrizni, hogy van-e, és mi van a db-ben
        model2 = QSqlQueryModel()
        query = QSqlQuery(f"SELECT * FROM reged_station where station_id = '{station_id}' or station_ip = '{ip_config}'", db=db)
        model2.setQuery(query)
        if model2.record(0).value(0):
            print("van")
        # else:
        #     model1 = QSqlTableModel()
        #     model1.setTable("reged_station")
        #     rec = model1.record()
        #     rec.remove(0)
        #     rec.setValue(0, station_id)
        #     rec.setValue(1, ip_config)
        #     rec.setValue(2, secret)
        #     if model1.insertRecord(-1, rec):
        #         model1.submitAll()
        #     else:
        #         db.rollback()

    def buttonbox_click(self, b):
        print(b.text())
        if b.text() == "Mentés":
            self.accept()
        elif b.text() == "Módosít":
            self.modify()
        else:
            self.reject()

    def modify(self):
        self.buttonbox.button(QDialogButtonBox.Ok).setDisabled(False)
        self.station.setDisabled(False)

    def accept(self):
        network = QSqlTableModel()
        network.setTable("reged_station")
        rec_net = network.record()
        rec_net.remove(0)
        rec_net.setValue(0, self.station.text())
        rec_net.setValue(1, self.ip.text())
        if network.insertRecord(-1, rec_net):
            network.submitAll()
        else:
            db.rollback()
        super().accept()

    def reject(self):
        super().reject()

# config['DEFAULT'] = {
#     'Station IP' : '192.168.68.3',
#     'Station Id' : 'tabla3'
# }
# config['MATCH_DEFAULTS'] = {
#     'Player 1' : 'Player_1',
#     'Player 2' : 'Player_2',
#     'Variant' : '501',
#     'Leg Number' : 3
# }
# with open('config.ini', 'w') as configfile:
#     config.write(configfile)


# print(config['DEFAULT'])
# for key in config['DEFAULT']:
#     print(key, config['DEFAULT'][key])
#
# print(config['DEFAULT'].get('station id',))

if __name__ == '__main__':
    app = QApplication([])
    win = NetworkSettingsDialog()
    win.show()
    app.exec_()