from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.RecordTapWidgets.CardShow import CardShow
from WorkWidgets.RecordTapWidgets.CardQuery import CardQuery
from WorkWidgets.RecordTapWidgets.CardAnalyz import CardAnalyz
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
        header_label = LabelComponent(16,"SwipeReport")
        backhome_botton = ButtonComponent("Home")
        backhome_botton.clicked.connect(lambda: self.backhome("home"))
        
        backhome_botton.setIcon(QtGui.QIcon('./icon/home.png'))
        backhome_botton.setIconSize(QtCore.QSize(25,25))
        backhome_botton.setObjectName('backhome_botton')
        
        layout.addWidget(header_label)
        layout.addStretch()
        layout.addWidget(backhome_botton)
        
        self.setLayout(layout)
    
class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget):
        super().__init__()
        self.taprecord_widget = update_widget
        layout = QtWidgets.QGridLayout()
        query_button = ButtonComponent(" search")
        show_button = ButtonComponent(" report")
        analysis_button = ButtonComponent(" analysis")
        query_button.clicked.connect(lambda: self.taprecord_widget("query"))
        show_button.clicked.connect(lambda: self.taprecord_widget("show"))
        analysis_button.clicked.connect(lambda: self.taprecord_widget("analysis"))
        query_button.setIcon(QtGui.QIcon('./icon/personal_search.png'))
        query_button.setIconSize(QtCore.QSize(30,40))
        show_button.setIcon(QtGui.QIcon('./icon/report.png'))
        show_button.setIconSize(QtCore.QSize(30,40))
        analysis_button.setIcon(QtGui.QIcon('./icon/analysis.png'))
        analysis_button.setIconSize(QtCore.QSize(30,40))
        
        layout.addWidget(show_button, 0,0,1,1)
        layout.addWidget(query_button, 1,0,1,1)
        layout.addWidget(analysis_button, 2,0,1,1)
        layout.setRowStretch(0,2)
        layout.setRowStretch(1,2)
        layout.setRowStretch(2,2)
        layout.setRowStretch(2,4)
        
        self.setLayout(layout)
        
class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.cardshow = CardShow()
        self.widget_dict = {
            "show": self.addWidget(self.cardshow),
            "query": self.addWidget(CardQuery(self.update_widget,self.cardshow.call_back_action)),
            "analysis": self.addWidget(CardAnalyz()),
        }
        self.update_widget("query")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()