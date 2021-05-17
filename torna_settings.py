import sys

from PySide2.QtWidgets import QApplication, QMessageBox, QDialog, QDialogButtonBox, QLabel, QLineEdit, QCheckBox, \
    QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QSpinBox, QCompleter
from PySide2.QtCore import *
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
import random

"""
When a QSqlDataBase is created using the addDatabase() method then the names passed through the connectionName 
parameter are stored in a dictionary where the key takes that value, if that parameter is not passed 
then "qt_sql_default_connection" is used causing the creation of the Second database you get a duplicate in the 
dictionary so Qt issues that warning. A possible solution is to pass it a different name (not tested):

def connectDb(database_name, connection_name):
    SERVER_NAME = "COMPUTER\\SQLEXPRESS"
    DATABASE_NAME = database_name
    connString = (
        f"DRIVER={{SQL Server}};" f"SERVER={SERVER_NAME};" f"DATABASE={DATABASE_NAME}"
    )
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE", connection_name)
    db.setDatabaseName(connString)
    if not db.open():
        print(db.lastError().text())
    return db

db1 = connectDb("Database1", "connection_1")
db2 = connectDb("Database2", "connection_2")

"""

db1 = QSqlDatabase.addDatabase('QMYSQL', 'database1')
db1.setHostName('192.168.68.22')
db1.setDatabaseName('cida')
db1.setUserName('cida')
db1.setPassword('cida')

# db = QSqlDatabase.addDatabase('QSQLITE', 'database2')
# db.setDatabaseName('scorer.db3')

db = db1

if not db.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        "Database Error: %s" % db.lastError().text(),
    )
    sys.exit(1)



class CustomSpinBox(QSpinBox):
    def __init__(self, min, max):
        super(CustomSpinBox, self).__init__()
        self.setMinimum(min)
        self.setMaximum(max)


class TornaSettingsDialog(QDialog):
    def __init__(self, parent = None, torna_id = None):
        super(TornaSettingsDialog, self).__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setWindowTitle("Verseny beállítások")
        self.torna_id = torna_id
        self.set_layouts()
        self.add_variables()
        self.alapertekek()
        self.add_buttonbox()

    def set_layouts(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.layout = QVBoxLayout()
        self.gomb_layout = QVBoxLayout()
        self.main_layout.addLayout(self.layout)
        self.main_layout.addLayout(self.gomb_layout)

    def add_variables(self):
        self.layout.addWidget(QLabel("A verseny megnevezése:"))
        self.torna_name = QLineEdit()
        self.torna_name.setPlaceholderText("A verseny megnevezése")
        self.layout.addWidget(self.torna_name)
        self.layout.addWidget(QLabel("Legyen csoportkör?"))
        self.is_roundrobin = QCheckBox()
        self.is_roundrobin.stateChanged.connect(self.roundrobin_changed)
        self.layout.addWidget(self.is_roundrobin)
        self.layout.addWidget(QLabel("Csoportok száma:"))
        self.csoport_number = CustomSpinBox(1, 16)
        self.layout.addWidget(self.csoport_number)
        self.layout.addWidget(QLabel("Játékosok száma csoportonként:"))
        self.jatekos_per_csoport = CustomSpinBox(3, 8)
        self.layout.addWidget(self.jatekos_per_csoport)
        self.layout.addWidget(QLabel("Játéknem:"))
        self.variant = CustomSpinBox(301, 1001)
        self.layout.addWidget(self.variant)
        self.layout.addWidget(QLabel("Set-ek?:"))
        self.is_sets = QCheckBox()
        self.is_sets.stateChanged.connect(self.is_sets_changed)
        self.layout.addWidget(self.is_sets)
        self.layout.addWidget(QLabel("Set-ek száma:"))
        self.sets_number = CustomSpinBox(1, 8)
        self.sets_number.setDisabled(True)
        self.layout.addWidget(self.sets_number)
        self.layout.addWidget(QLabel("Leg-ek száma:"))
        self.legs_number = CustomSpinBox(2, 30)
        self.layout.addWidget(self.legs_number)
        self.layout.addWidget(QLabel("Best of..."))
        self.is_best = QCheckBox()
        self.layout.addWidget(self.is_best)
        self.layout.addWidget(QLabel("Döntetlen"))
        self.is_draw = QCheckBox()
        self.is_draw.stateChanged.connect(self.is_draw_changed)
        self.layout.addWidget(self.is_draw)
        self.layout.addWidget(QLabel("Pont(Győzelem):"))
        self.pont_win = CustomSpinBox(2, 5)
        self.layout.addWidget(self.pont_win)
        self.layout.addWidget(QLabel("Pont(Döntetlen):"))
        self.pont_draw = CustomSpinBox(1, 3)
        self.pont_draw.setDisabled(True)
        self.layout.addWidget(self.pont_draw)
        self.layout.addWidget(QLabel("Pont(Vereség):"))
        self.pont_lost = CustomSpinBox(0, 2)
        self.layout.addWidget(self.pont_lost)
        self.layout.addWidget(QLabel("Főág"))
        self.is_single_elim = QCheckBox()
        self.is_single_elim.stateChanged.connect(self.is_single_changed)
        self.layout.addWidget(self.is_single_elim)
        self.layout.addWidget(QLabel("Főág száma:"))
        self.num_single = CustomSpinBox(4, 128)
        self.num_single.setDisabled(True)
        self.layout.addWidget(self.num_single)
        self.layout.addWidget(QLabel("Leg-ek száma a főágon:"))
        self.leg_num_single = CustomSpinBox(3, 20)
        self.leg_num_single.setDisabled(True)
        self.layout.addWidget(self.leg_num_single)
        self.layout.addWidget(QLabel("Leg-ek száma az elődöntőben:"))
        self.leg_num_semifinal = CustomSpinBox(4, 20)
        self.leg_num_semifinal.setDisabled(True)
        self.layout.addWidget(self.leg_num_semifinal)
        self.layout.addWidget(QLabel("Leg-ek száma a döntőben:"))
        self.leg_num_final = CustomSpinBox(5, 20)
        self.leg_num_final.setDisabled(True)
        self.layout.addWidget(self.leg_num_final)
        self.layout.addWidget(QLabel("3. hely kijátszva"))
        self.is_3place = QCheckBox()
        self.is_3place.stateChanged.connect(self.is_3place_changed)
        self.is_3place.setDisabled(True)
        self.layout.addWidget(self.is_3place)
        self.layout.addWidget(QLabel("Leg-ek száma a 3. helyért:"))
        self.leg_num_3place = CustomSpinBox(4, 20)
        self.leg_num_3place.setDisabled(True)
        self.layout.addWidget(self.leg_num_3place)

    def alapertekek(self):
        if not self.torna_id:
            self.torna_name.clear()
            self.is_roundrobin.setChecked(True)
            self.csoport_number.setValue(1)
            self.jatekos_per_csoport.setValue(4)
            self.variant.setValue(501)
            self.is_sets.setChecked(False)
            self.sets_number.setValue(1)
            self.legs_number.setValue(2)
            self.is_best.setChecked(False)
            self.is_draw.setChecked(False)
            self.pont_win.setValue(2)
            self.pont_draw.setValue(1)
            self.pont_lost.setValue(0)
            self.is_single_elim.setChecked(False)
            self.num_single.setValue(8)
            self.leg_num_single.setValue(3)
            self.leg_num_semifinal.setValue(4)
            self.leg_num_final.setValue(5)
            self.is_3place.setChecked(False)
            self.leg_num_3place.setValue(4)
        else:
            model = QSqlTableModel(db=db)
            model.setTable("torna_settings")
            model.setFilter(f"torna_id={self.torna_id}")
            model.select()
            print(model.record(0))
            self.torna_name.setText(model.record(0).value(1))
            self.is_roundrobin.setChecked(model.record(0).value(2))
            self.csoport_number.setValue(model.record(0).value(3))
            self.jatekos_per_csoport.setValue(model.record(0).value(4))
            self.variant.setValue(int(model.record(0).value(5)))
            self.is_sets.setChecked(model.record(0).value(6))
            self.sets_number.setValue(model.record(0).value(7))
            self.legs_number.setValue(model.record(0).value(8))
            self.is_best.setChecked(model.record(0).value(9))
            self.is_draw.setChecked(model.record(0).value(10))
            self.pont_win.setValue(model.record(0).value(11))
            self.pont_draw.setValue(model.record(0).value(12))
            self.pont_lost.setValue(model.record(0).value(13))
            self.is_single_elim.setChecked(model.record(0).value(14))
            self.num_single.setValue(model.record(0).value(15))
            self.leg_num_single.setValue(model.record(0).value(17))
            self.leg_num_semifinal.setValue(model.record(0).value(18))
            self.leg_num_final.setValue(model.record(0).value(20))
            self.is_3place.setChecked(model.record(0).value(16))
            self.leg_num_3place.setValue(model.record(0).value(19))

    def add_buttonbox(self):
        self.buttonbox = QDialogButtonBox()
        self.buttonbox.setOrientation(Qt.Vertical)
        self.buttonbox.addButton("Mentés", QDialogButtonBox.ActionRole)
        self.buttonbox.addButton("Alaphelyzet", QDialogButtonBox.ActionRole)
        self.gomb_members = QPushButton("Résztvevők")
        self.gomb_members.setDisabled(True)
        self.buttonbox.addButton(self.gomb_members, QDialogButtonBox.ActionRole)
        self.gomb_tabella = QPushButton("Tabella")
        self.gomb_tabella.setDisabled(True)
        self.buttonbox.addButton(self.gomb_tabella, QDialogButtonBox.ActionRole)
        self.buttonbox.addButton("Mégsem", QDialogButtonBox.ActionRole)
        self.buttonbox.clicked.connect(self.buttonbox_click)
        self.gomb_layout.addWidget(self.buttonbox)

    def roundrobin_changed(self, state):
        if state == Qt.Checked:
            self.csoport_number.setDisabled(False)
            self.jatekos_per_csoport.setDisabled(False)
        else:
            self.csoport_number.setDisabled(True)
            self.jatekos_per_csoport.setDisabled(True)

    def is_sets_changed(self, state):
        if state == Qt.Checked:
            self.sets_number.setDisabled(False)
        else:
            self.sets_number.setDisabled(True)

    def is_draw_changed(self, state):
        if state == Qt.Checked:
            self.pont_draw.setDisabled(False)
        else:
            self.pont_draw.setDisabled(True)

    def is_single_changed(self, state):
        # a főághoz kapcsolódó paraméterek tiltása/engedélyezése
        if state == Qt.Checked:
            self.num_single.setDisabled(False)
            self.is_3place.setDisabled(False)
            self.leg_num_single.setDisabled(False)
            self.leg_num_semifinal.setDisabled(False)
            if self.is_3place.isChecked():
                self.leg_num_3place.setDisabled(False)
            else:
                self.leg_num_3place.setDisabled(True)
            self.leg_num_final.setDisabled(False)
        else:
            self.num_single.setDisabled(True)
            self.is_3place.setDisabled(True)
            self.leg_num_single.setDisabled(True)
            self.leg_num_semifinal.setDisabled(True)
            self.leg_num_3place.setDisabled(True)
            self.leg_num_final.setDisabled(True)

    def is_3place_changed(self, state):
        if state == Qt.Checked:
            self.leg_num_3place.setDisabled(False)
        else:
            self.leg_num_3place.setDisabled(True)

    def buttonbox_click(self, b):
        if b.text() == "Mentés":
            self.save()
        elif b.text() == "Alaphelyzet":
            self.alapertekek()
        elif b.text() == "Résztvevők":
            self.members()
        elif b.text() == "Tabella":
            self.tabella()
        elif b.text() == "Mégsem":
            self.reject()
        else:
            pass

    def save(self):
        if not self.torna_id:
            self.insert_torna_settings()
        else:
            self.update_torna_settings()

    def insert_torna_settings(self):
        van_ilyen_nev = False
        if len(self.torna_name.text()) != 0:
            torna_id_model = QSqlQueryModel()
            query = QSqlQuery("select torna_id, torna_name from torna_settings", db=db)
            torna_id_model.setQuery(query)
            for i in range(torna_id_model.rowCount()):
                if torna_id_model.record(i).value(1) == self.torna_name.text():
                    msg = QMessageBox(self)
                    msg.setStyleSheet("fonz-size: 20px")
                    msg.setWindowTitle("Név ütközés!")
                    msg.setText(
                        '<html style="font-size: 14px; color: red">Már van ilyen nevű verseny!<br></html>' + '<html style="font-size: 16px">Kérem adjon a versenynek egyedi nevet!</html>')
                    msg.exec_()
                    van_ilyen_nev = True
            if not van_ilyen_nev:
                torna_settings_model = QSqlTableModel(db=db)  # !!!!!!! Ha több db van, akkor itt konkrétan meg kell adni
                torna_settings_model.setTable("torna_settings")
                record = torna_settings_model.record()

                record.setValue(1, self.torna_name.text())
                if self.is_roundrobin.isChecked():
                    record.setValue(2, 1)
                else:
                    record.setValue(2, 0)
                record.setValue(3, self.csoport_number.value())
                record.setValue(4, self.jatekos_per_csoport.value())
                record.setValue(5, self.variant.value())
                if self.is_sets.isChecked():
                    record.setValue(6, 1)
                else:
                    record.setValue(6, 0)
                record.setValue(7, self.sets_number.value())
                record.setValue(8, self.legs_number.value())
                # print(record.value(2))
                if self.is_best.isChecked():
                    record.setValue(9, 1)
                else:
                    record.setValue(9, 0)
                if self.is_draw.isChecked():
                    record.setValue(10, 1)
                else:
                    record.setValue(10, 0)
                record.setValue(11, self.pont_win.value())
                record.setValue(12, self.pont_draw.value())
                record.setValue(13, self.pont_lost.value())
                if self.is_single_elim.isChecked():
                    record.setValue(14, 1)
                else:
                    record.setValue(14,0)
                record.setValue(15, self.num_single.value())
                if self.is_3place.isChecked():
                    record.setValue(16, 1)
                else:
                    record.setValue(16,0)
                record.setValue(17, self.leg_num_single.value())
                record.setValue(18, self.leg_num_semifinal.value())
                record.setValue(19, self.leg_num_3place.value())
                record.setValue(20, self.leg_num_final.value())
                record.setValue(21,2)
                # aktiv flag:  0: vége, 1: folyamatban, 2: szerkesztés alatt
                # print(record)
                if torna_settings_model.insertRecord(-1, record):
                    torna_settings_model.submitAll()
                else:
                    db.rollback()

                torna_id_model2 = QSqlQueryModel()
                query2 = QSqlQuery(f"select torna_id from torna_settings where torna_name='{self.torna_name.text()}'", db=db)
                torna_id_model2.setQuery(query2)
                self.torna_id = int(torna_id_model2.record(0).value(0))
                self.gomb_members.setDisabled(False)
        else:
            msg = QMessageBox(self)
            msg.setStyleSheet("fonz-size: 20px")
            msg.setWindowTitle("Hiányzik a verseny neve!")
            msg.setText(
                '<html style="font-size: 14px; color: red">A létrehozott versenynek kell egy elnevezés!<br></html>' + '<html style="font-size: 16px">Kérem adja meg a verseny nevét!</html>')
            msg.exec_()

    def update_torna_settings(self):
        torna_settings_model = QSqlTableModel(db=db)
        torna_settings_model.setTable("torna_settings")
        record = torna_settings_model.record()
        torna_settings_model.select()
        # for x in range(torna_settings_model.rowCount()):
        #     record.setGenerated(x, False)
        record.setValue(0, self.torna_id)
        record.setValue(1, self.torna_name.text())
        if self.is_roundrobin.isChecked():
            record.setValue(2, 1)
        else:
            record.setValue(2, 0)
        record.setValue(3, self.csoport_number.value())
        record.setValue(4, self.jatekos_per_csoport.value())
        record.setValue(5, self.variant.value())
        if self.is_sets.isChecked():
            record.setValue(6, 1)
        else:
            record.setValue(6, 0)
        record.setValue(7, self.sets_number.value())
        record.setValue(8, self.legs_number.value())
        if self.is_best.isChecked():
            record.setValue(9, 1)
        else:
            record.setValue(9, 0)
        if self.is_draw.isChecked():
            record.setValue(10, 1)
        else:
            record.setValue(10, 0)
        record.setValue(11, self.pont_win.value())
        record.setValue(12, self.pont_draw.value())
        record.setValue(13, self.pont_lost.value())
        if self.is_single_elim.isChecked():
            record.setValue(14, 1)
        else:
            record.setValue(14, 0)
        record.setValue(15, self.num_single.value())
        if self.is_3place.isChecked():
            record.setValue(16, 1)
        else:
            record.setValue(16, 0)
        record.setValue(17, self.leg_num_single.value())
        record.setValue(18, self.leg_num_semifinal.value())
        record.setValue(19, self.leg_num_3place.value())
        record.setValue(20, self.leg_num_final.value())
        record.setValue(21, 2)

        for i in range(torna_settings_model.rowCount()):
            if torna_settings_model.record(i).value(0) == self.torna_id:
                print(torna_settings_model.record(i).value(0), ":", i)
                record_number = i
        print(record)
        if torna_settings_model.setRecord(record_number, record):
            torna_settings_model.submitAll()
        else:
            db.rollback()

    def members(self):
        # todo Itt kell a verseny résztvevőit öszerakni
        pass

    def tabella(self):
        # todo Itt kell a sorsolást, tabella összeállítást megcsinálni
        pass

    def accept(self):
        # todo Ez majd csak a bezáráshoz kell
        super().accept()

    def reject(self):
        print("CANCEL")
        super().reject()

if __name__ == '__main__':
    app = QApplication([])
    win = TornaSettingsDialog()
    win.show()
    app.exec_()