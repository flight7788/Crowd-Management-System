from WorkWidgets.MainWidget import MainWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import sip
import sys

app = QApplication([])
main_window = MainWidget()

#main_window.setFixedSize(1000, 500)
main_window.show()
# main_window.showFullScreen()

sys.exit(app.exec_())
