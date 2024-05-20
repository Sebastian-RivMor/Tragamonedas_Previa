import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\Project\\inicio.ui', self)
        self.background_inicio.setPixmap(QPixmap("C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\Welcome.png"))
        self.button_Inicio.clicked.connect(self.show_slot)  # Conectar el botón con el método show_slot

    def show_slot(self):
        self.slot_window = SlotWindow()
        self.slot_window.show()
        self.close()  # Cerrar la ventana principal

class SlotWindow(QWidget):

    def __init__(self):
        super(SlotWindow, self).__init__()
        loadUi('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\Project\\slot.ui', self)
        self.setStyleSheet("background-image: url(C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\background.qrc.jpg)")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
