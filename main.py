import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic


class MyInterface(QMainWindow):
    def __init__(self):
        super(MyInterface, self).__init__()
        uic.loadUi('interface_SBD.ui', self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = MyInterface()
    interface.show()
    sys.exit(app.exec_())
