from gc import callbacks
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.CameraWidget import CameraWidget


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")

        function_widget = FunctionWidget({'camera':CameraWidget()})
        function_widget.widget_dict['camera'].detect_face = True

        menu_widget = MenuWidget(function_widget)
        menu_widget.setStyleSheet("background-color: rgb(61, 80, 95)")
        
        layout_center = QtWidgets.QVBoxLayout()
        layout_center.addWidget(menu_widget, stretch=15)
        layout_center.addWidget(function_widget, stretch=85)
        layout_center.setSpacing(10)

        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(24, "NTUT Crowd Management System")
            
        layout.addWidget(header_label, stretch=20)
        layout.addLayout(layout_center, stretch=80)

        self.setLayout(layout)


class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget):
        super().__init__()
        self.setObjectName("menu_widget")
        
        layout = QtWidgets.QHBoxLayout()
        setting_button = ButtonComponent(" Setting", 20)
        setting_button.setIcon(QtGui.QIcon('./icon/setting.png'))
        setting_button.setIconSize(QtCore.QSize(50,50))
        currentLog_button = ButtonComponent(" Current log", 20)
        currentLog_button.setIcon(QtGui.QIcon('./icon/server.png'))
        currentLog_button.setIconSize(QtCore.QSize(50,50))
        #start_button.clicked.connect()
        #stop_button.clicked.connect()

        layout.addWidget(setting_button, stretch=1)
        layout.addWidget(currentLog_button, stretch=1)

        self.setLayout(layout)
  


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self, MyWidget):
        super().__init__()
        self.widget_dict = MyWidget
        self.widget_layer_dict = {}
        for name, widget in MyWidget.items():
            self.widget_layer_dict[name] = self.addWidget(widget)
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_layer_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()

