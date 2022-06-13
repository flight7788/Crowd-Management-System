from PyQt5 import QtWidgets,QtCore,QtWidgets
from WorkWidgets.HomeWidget import HomeWidget
from WorkWidgets.ManageWidgets.ManageStuWidget import ManageStuWidget
from WorkWidgets.RecordTapWidgets.RecodeTapWidget import RecodeTapWidget
import os


class MainWidget(QtWidgets.QStackedWidget):
    def __init__(self,app_close):
        super().__init__()
        self.app_close = app_close
        self.setStyleSheet("background-color: rgb(33, 43, 51)")
        self.widget_dict = {
            "home": self.addWidget(HomeWidget(self.update_widget)),
            "ManageStu": self.addWidget(ManageStuWidget(self.update_widget)),
            "RecodeTap": self.addWidget(RecodeTapWidget(self.update_widget)),
        }
        self.update_widget("home")

    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()
    
    def closeEvent(self, event):
        self.app_close()
        path = "./Image"
        files = os.listdir(path)
        for f in files:
            if f.endswith(".png"):
                os.remove(os.path.join(path,f))
        