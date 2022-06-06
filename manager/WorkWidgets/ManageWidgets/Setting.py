from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.ManageWidgets.StuModify import StuModify
from WorkWidgets.ManageWidgets.StuQuery import StuQuery
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

class Setting(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.modify = StuModify(self.update_widget)
        self.widget_dict = {
            "query": self.addWidget(StuQuery(self.update_widget,self.modify.getinfo)),
            "modify": self.addWidget(self.modify)
        }
        self.update_widget("query")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()
    
    def load(self):
        pass