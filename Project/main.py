import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class Mywindow(QMainWindow):

    def __init__(self):
        super(Mywindow, self).__init__()
        loadUi('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\Project\\design.ui', self)



        self.Buttoncont. clicked. connect(self.incrementar_numero)

        # Inicializa el ndmero en @
        self.numero = 0

    def incrementar_numero(self):
        # Aumenta el nimero en 1y actualiza el label
        self.numero += 1
        self.label_cont.setText(str(self.numero))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Mywindow()
    window.show()
    sys.exit(app.exec())

