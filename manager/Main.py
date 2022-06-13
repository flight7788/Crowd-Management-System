from WorkWidgets.MainWidget import MainWidget
from PyQt5.QtWidgets import QApplication
import sys

class managerQT:
    def __init__(self):
        self.app = QApplication([])
    
    def execute(self):
        main_window = MainWidget(self.close_window)
        #main_window.setFixedSize(900, 500)
        main_window.show()
        # main_window.showFullScreen()
        sys.exit(self.app.exec_())

    def close_window(self):
        self.app.closeAllWindows()
        
if __name__ == "__main__":
    manageQT = managerQT()
    manageQT.execute()