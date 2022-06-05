from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.HomeWidget import HomeWidget
from WorkWidgets.ManageWidgets.ManageStuWidget import ManageStuWidget
from WorkWidgets.RecordTapWidgets.RecodeTapWidget import RecodeTapWidget
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent


class MainWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
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