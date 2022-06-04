from WorkWidgets.MainWidget import MainWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import sip
import sys

  
if __name__=='__main__':
    app = QApplication([])
    main_window = MainWidget()
    main_window.setStyleSheet("background-color: rgb(33, 43, 51)")
    #main_window.setFixedSize(1200, 900)
    main_window.show()
    sys.exit(app.exec_())

