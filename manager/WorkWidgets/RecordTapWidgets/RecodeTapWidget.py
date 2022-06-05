from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.RecordTapWidgets.CardShow import CardShow
from WorkWidgets.RecordTapWidgets.CardQuery import CardQuery
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

class RecodeTapWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.backhome = update_widget_callback
        layout = QtWidgets.QGridLayout()
        header_widget = HeaderWidget(self.backhome)
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)
        function_widget.setStyleSheet("background-color: rgb(61, 80, 95)")
        
        layout.addWidget(header_widget, 0,0,1,2)
        layout.addWidget(menu_widget, 1,0,1,1)
        layout.addWidget(function_widget, 1,1,1,1)
        
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,9)
        layout.setRowStretch(0,1)
        layout.setRowStretch(1,9)

        self.setLayout(layout)
        
    def load(self):
        pass
    
class HeaderWidget(QtWidgets.QWidget):
    def __init__(self, backhome):
        super().__init__()
        self.backhome = backhome
        layout = QtWidgets.QHBoxLayout()
        header_label = LabelComponent(16,"刷卡報表")
        backhome_botton = ButtonComponent("首頁")
        backhome_botton.clicked.connect(lambda: self.backhome("home"))
        
        backhome_botton.setIcon(QtGui.QIcon('./icon/home.png'))
        backhome_botton.setIconSize(QtCore.QSize(25,25))
        
        layout.addWidget(header_label)
        layout.addStretch()
        layout.addWidget(backhome_botton)
        
        self.setLayout(layout)
    
class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget):
        super().__init__()
        self.taprecord_widget = update_widget
        layout = QtWidgets.QGridLayout()
        query_botton = ButtonComponent("人員查詢")
        showAll_botton = ButtonComponent("紀錄查詢")
        query_botton.clicked.connect(lambda: self.taprecord_widget("query"))
        showAll_botton.clicked.connect(lambda: self.taprecord_widget("show"))
        
        layout.addWidget(showAll_botton, 0,0,1,1)
        layout.addWidget(query_botton, 1,0,1,1)
        layout.setRowStretch(0,2)
        layout.setRowStretch(1,2)
        layout.setRowStretch(2,6)
        
        self.setLayout(layout)
        
class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "show": self.addWidget(CardShow()),
            "query": self.addWidget(CardQuery()),
        }
        self.update_widget("query")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()