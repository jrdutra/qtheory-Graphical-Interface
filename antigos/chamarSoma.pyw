from PyQt5 import QtWidgets
from soma import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
import sys

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnPlus.clicked.connect(self.on_click)
    
    @pyqtSlot()
    def on_click(self):
        
        n1 = float(self.ui.txt1.text())
        n2 = float(self.ui.txt2.text())
        res = n1 + n2
        self.ui.lblResult.setText(str(res))


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()