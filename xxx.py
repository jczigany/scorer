from PySide2.QtWidgets import QMainWindow, QDialog, QVBoxLayout, QPushButton, QApplication, QWidget, QLabel
from PySide2.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("Test Window")

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        button = QPushButton("New Game")
        main_layout.addWidget(button)
        main_layout.setAlignment(button, Qt.AlignTop)

        self.game_window = GameWindow(self)
        self.start_game_dialog = StartGameWindow(self)
        self.start_game_dialog.accepted.connect(self._new_game_started)
        self.start_game_dialog.rejected.connect(self._new_game_rejected)

        # button.clicked.connect(self.start_game_dialog.show)
        button.clicked.connect(self.start)
        # self.game_window.show()
        # self.start_game_dialog.show()
        self.start()

    def start(self):
        self.game_window.show()
        self.start_game_dialog.show()

    def _new_game_started(self):
        print("New game started")
        print(self.start_game_dialog.var1)
        self.game_window.show()

    def _new_game_rejected(self):
        print("New game rejected")
        print(self.start_game_dialog.var1)
        self.game_window.close()


class GameWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        self.resize(300, 200)
        self.setWindowTitle("Game Window")

        main_layout.addWidget(QLabel("Game Window"))


class StartGameWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New Game")
        main_layout = QVBoxLayout(self)
        self.setModal(True)
        self.var1 = "settings parameter"
        main_layout.addWidget(QLabel("Start New Game"))

        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")

        main_layout.addWidget(ok_button)
        main_layout.addWidget(cancel_button)

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()