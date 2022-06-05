from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.ManageWidgets.StuModify import StuModify
from WorkWidgets.ManageWidgets.StuQuery import StuQuery
from WorkWidgets.ManageWidgets.StuShow import StuShow
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

class Management(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)
        #function_widget.setStyleSheet("background-color: rgb(255, 80, 95)")
        layout.addWidget(menu_widget, stretch=1)
        layout.addWidget(function_widget,stretch=9)

        self.setLayout(layout)
        
    def load(self):
        pass
    
    
class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget):
        super().__init__()
        self.stufunction_widget = update_widget
        layout = QtWidgets.QHBoxLayout()
        label = LabelComponent(12,"查詢:")
        query_radio_button = QtWidgets.QRadioButton('query')
        query_radio_button.toggled.connect(lambda: self.stufunction_widget("query"))
        show_radio_button = QtWidgets.QRadioButton('show all student')
        show_radio_button.toggled.connect(lambda: self.stufunction_widget("show"))
        show_radio_button.setChecked(True)
        query_radio_button.setStyleSheet("color: rgb(255, 255, 255);")
        show_radio_button.setStyleSheet("color: rgb(255, 255, 255);")
        
        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(show_radio_button)
        layout.addWidget(query_radio_button)
        layout.addStretch(10)
        
        self.setLayout(layout)
        
class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.modify = StuModify(self.update_widget)
        self.widget_dict = {
            "query": self.addWidget(StuQuery(self.update_widget,self.modify.getinfo)),
            "show": self.addWidget(StuShow()),
            "modify": self.addWidget(self.modify)
        }
        self.update_widget("show")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()