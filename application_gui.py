from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton, QTextEdit
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal

from mock import AnalisisVoz

from microphone_manager import MicrophoneManager
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.abspath("./resources/ui/main.ui")
        uic.loadUi(ui_path,self)

        self.analizador_voz = AnalisisVoz()

        self.analizador_voz.texto_actual_signal.connect(self.actualizar_texto)
        self.analizador_voz.texto_traducido_signal.connect(self.actualizar_texto_traducido)
        self.analizador_voz.emocion_actual_signal.connect(self.actualizar_emocion)

        self.microphone_manager = MicrophoneManager()
        self.populate_microphone_list()

        self.bt_grabar.clicked.connect(self.on_bt_grabar_clicked)
        self.bt_stop.clicked.connect(self.on_bt_stop_clicked)
        self.cb_inputList.currentIndexChanged.connect(self.on_microphone_selected)
        self.cb_language.currentIndexChanged.connect(self.on_microphone_selected)
    
        self.show()

   # Funciones para actualizar la interfaz
    def actualizar_texto(self, texto):
        self.tf_textoTranscrito.setText(texto)

    def actualizar_texto_traducido(self, texto):
        self.tf_textoTraducido.setText(texto)

    def actualizar_emocion(self, emocion):
        self.label_4.setText(emocion)

    # Eventos
    def on_bt_grabar_clicked(self):
        self.lb_status.setText("Grabando...")
        self.cb_inputList.setEnabled(False)
        self.cb_language.setEnabled(False)
        
        if not self.analizador_voz.isRunning():
            self.analizador_voz.start()
            

    def on_bt_stop_clicked(self):
        self.lb_status.setText("Parado")
        self.cb_inputList.setEnabled(True)
        self.cb_language.setEnabled(False)
        
        # Detener el análisis en segundo plano
        if self.analizador_voz.isRunning():
            self.analizador_voz.detener_transcribir_desde_microfono()
    

    def on_microphone_selected(self):
        selected_index = self.cb_inputList.currentData()
        if self.microphone_manager.select_microphone(selected_index):
            selected_microphone = self.microphone_manager.get_selected_microphone()
            print(f"Micrófono seleccionado: {selected_microphone}")
        else:
            print("Error al seleccionar el micrófono.")

    

    # funciones
    def populate_microphone_list(self):
        microphones = self.microphone_manager.get_microphone_list()
        self.cb_inputList.clear()
        for name, index in microphones:
            self.cb_inputList.addItem(name, index)

def initialize_window(argv: list[str]):
    app = QApplication(argv)
    UIWindow = MainWindow()
    UIWindow.setWindowTitle('Super Transcriptor Paralelo 64');
    app.exec_()
    

