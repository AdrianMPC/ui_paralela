from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QTextEdit
from PyQt5 import uic

from microphone_manager import MicrophoneManager
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.abspath("./resources/ui/main.ui")
        uic.loadUi(ui_path,self)

        self.microphone_manager = MicrophoneManager()
        self.populate_microphone_list()
 
        self.bt_grabar.clicked.connect(self.on_bt_grabar_clicked)
        self.bt_stop.clicked.connect(self.on_bt_stop_clicked)
        self.cb_inputList.currentIndexChanged.connect(self.on_microphone_selected)
        self.show()

    # Eventos
    def on_bt_grabar_clicked(self):
        self.lb_status.setText("Grabando...")

    def on_bt_stop_clicked(self):
        self.lb_status.setText("Parado")

    def on_microphone_selected(self):
        selected_index = self.cb_inputList.currentData()
        if self.microphone_manager.select_microphone(selected_index):
            selected_microphone = self.microphone_manager.get_selected_microphone()
            print(f"Micrófono seleccionado: {selected_microphone}")
        else:
            print("Error al seleccionar el micrófono.")

    # funciones
    def populate_microphone_list(self):
        """Llena el combo box con los micrófonos detectados."""
        microphones = self.microphone_manager.get_microphone_list()
        self.cb_inputList.clear()
        for name, index in microphones:
            self.cb_inputList.addItem(name, index)

def initialize_window(argv: list[str]):
    app = QApplication(argv)
    UIWindow = MainWindow()
    app.exec_()
    

