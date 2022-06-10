from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.ManageWidgets.StuAdd import StuAdd
from WorkWidgets.ManageWidgets.StuShow import StuShow
from WorkWidgets.ManageWidgets.Setting import Setting
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

class ManageStuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.backhome = update_widget_callback
        layout = QtWidgets.QVBoxLayout()
        self.function_widget = FunctionWidget()
        self.menu_widget = MenuWidget(self.function_widget.update_widget,self.function_widget.Stushow.refresh,self.backhome)
        self.function_widget.setStyleSheet("background-color: rgb(61, 80, 95)")
        
        layout.addWidget(self.menu_widget, stretch=1)
        layout.addWidget(self.function_widget,stretch=9)

        self.setLayout(layout)
        
    def load(self):
        self.menu_widget.show_action()
    
class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget,show_refresh,backhome):
        super().__init__()
        self.backhome = backhome
        self.show_refresh =show_refresh
        self.stufunction_widget = update_widget
        layout = QtWidgets.QHBoxLayout()
        label = LabelComponent(14,"|")
        label2 = LabelComponent(14,"|")
        self.show_botton = ButtonComponent("MemberList")
        self.addstu_botton = ButtonComponent("Add")
        self.modifystu_botton = ButtonComponent("Setting")
        self.refresh_botton = ButtonComponent("")
        backhome_botton = ButtonComponent("Home")
        self.button_style = buttonstyle()
        self.show_botton.clicked.connect(lambda: self.show_action())
        self.addstu_botton.clicked.connect(lambda: self.add_action())
        self.modifystu_botton.clicked.connect(lambda: self.modifystu_action())
        self.refresh_botton.clicked.connect(lambda: self.refresh_action())
        backhome_botton.clicked.connect(lambda: self.backhome("home"))
        
        self.show_botton.setObjectName('show_botton')
        self.addstu_botton.setObjectName('addstu_botton')
        self.modifystu_botton.setObjectName('modifystu_botton')
        
        self.show_botton.setIcon(QtGui.QIcon('./icon/StuList.png'))
        self.show_botton.setIconSize(QtCore.QSize(25,25))
        self.addstu_botton.setIcon(QtGui.QIcon('./icon/StuAdd.png'))
        self.addstu_botton.setIconSize(QtCore.QSize(25,25))
        self.modifystu_botton.setIcon(QtGui.QIcon('./icon/StuSetting.png'))
        self.modifystu_botton.setIconSize(QtCore.QSize(25,25))
        backhome_botton.setIcon(QtGui.QIcon('./icon/home.png'))
        backhome_botton.setIconSize(QtCore.QSize(25,25))
        self.refresh_botton.setIcon(QtGui.QIcon('./icon/refresh.png'))
        self.refresh_botton.setIconSize(QtCore.QSize(25,25))
        
        layout.addWidget(self.show_botton)
        layout.addWidget(label)
        layout.addWidget(self.modifystu_botton)
        layout.addWidget(label2)
        layout.addWidget(self.addstu_botton)
        layout.addStretch()
        layout.addWidget(self.refresh_botton)
        layout.addWidget(backhome_botton)
        
        self.setLayout(layout)
    
    def refresh_action(self):
        self.show_refresh()
    def modifystu_action(self):
        self.modifystu_botton.setStyleSheet(self.button_style.SetStyle('modifystu_botton',"markstyle"))
        self.addstu_botton.setStyleSheet(self.button_style.SetStyle('addstu_botton'))
        self.show_botton.setStyleSheet(self.button_style.SetStyle('show_botton'))
        self.refresh_botton.hide()
        self.stufunction_widget("setting")
    def add_action(self):
        self.modifystu_botton.setStyleSheet(self.button_style.SetStyle('modifystu_botton'))
        self.addstu_botton.setStyleSheet(self.button_style.SetStyle('addstu_botton',"markstyle"))
        self.show_botton.setStyleSheet(self.button_style.SetStyle('show_botton'))
        self.refresh_botton.hide()
        self.stufunction_widget("add")
    def show_action(self):
        self.modifystu_botton.setStyleSheet(self.button_style.SetStyle('modifystu_botton'))
        self.addstu_botton.setStyleSheet(self.button_style.SetStyle('addstu_botton'))
        self.show_botton.setStyleSheet(self.button_style.SetStyle('show_botton',"markstyle"))
        self.refresh_botton.show()
        self.stufunction_widget("show")

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.Stushow =StuShow()
        self.widget_dict = {
            "show": self.addWidget(self.Stushow),
            "add": self.addWidget(StuAdd()),
            "setting": self.addWidget(Setting())
        }
        self.update_widget("show")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()

class buttonstyle():
    def __init__(self):
        pass
    
    def SetStyle(self,button,style="normalstyle"):
        if style == "markstyle":
            background_color = "rgb(200, 200, 200)"
            color = "black"
        else:
            background_color = "rgb(33, 43, 51)"
            color = "white"
        
        set_style = """
            QPushButton#{}{{
                background-color: {};
                border-radius: 5px;
                color: {};
            }}
            QPushButton#{}:hover {{
                background-color: rgb(200, 200, 200);
                color: black;
                border-radius: 10px;
            }}
        """.format(button,background_color,color,button)
        return set_style
