from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.ManageWidgets.StuAdd import StuAdd
from WorkWidgets.ManageWidgets.Management import Management
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

class ManageStuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.backhome = update_widget_callback
        layout = QtWidgets.QVBoxLayout()
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget,self.backhome)
        function_widget.setStyleSheet("background-color: rgb(61, 80, 95)")
        
        layout.addWidget(menu_widget, stretch=1)
        layout.addWidget(function_widget,stretch=9)

        self.setLayout(layout)
        
    def load(self):
        pass
    
    
class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget,backhome):
        super().__init__()
        self.backhome = backhome
        self.stufunction_widget = update_widget
        layout = QtWidgets.QHBoxLayout()
        query_botton = ButtonComponent("人員資料")
        addstu_botton = ButtonComponent("新增人員")
        backhome_botton = ButtonComponent("首頁")
        query_botton.clicked.connect(lambda: self.stufunction_widget("management"))
        addstu_botton.clicked.connect(lambda: self.stufunction_widget("add"))
        backhome_botton.clicked.connect(lambda: self.backhome("home"))
        
        backhome_botton.setIcon(QtGui.QIcon('./icon/home.png'))
        backhome_botton.setIconSize(QtCore.QSize(30,30))
        
        layout.addWidget(query_botton)
        layout.addWidget(addstu_botton)
        layout.addStretch()
        layout.addWidget(backhome_botton)
        
        self.setLayout(layout)
        
class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "management": self.addWidget(Management()),
            "add": self.addWidget(StuAdd()),
        }
        self.update_widget("management")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()