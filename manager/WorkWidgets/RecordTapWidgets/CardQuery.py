from inspect import Parameter
from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class CardQuery(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.stack_widget = stackWidget()
        layout.addWidget(self.stack_widget)
        self.setLayout(layout)
        
    def load(self):
        self.stack_widget.update_widget("query")
    
class stackWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.respone = Respone(self.update_widget)
        self.widget_dict = {
            "query": self.addWidget(Query(self.update_widget,self.respone.getInfo)),
            "respone": self.addWidget(self.respone),
        }
        self.update_widget("query")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()

class Query(QtWidgets.QWidget):
    def __init__(self,update_widget,respone):
        super().__init__()
        self.update_widget = update_widget
        self.respone = respone
        layout = QtWidgets.QGridLayout()
        
        stuid_label = LabelComponent(16,"學號:")
        self.stuid_input = LineEditComponent("")
        query = ButtonComponent("查詢")
        query.clicked.connect(self.query_action)
        
        layout.addWidget(stuid_label, 1,1,1,1)
        layout.addWidget(self.stuid_input, 1,2,1,1)
        layout.addWidget(query, 1,3,1,1)
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 2)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 6)
        self.setLayout(layout)
    
    def load(self):
        pass
    
    def query_action(self):
        stuid = self.stuid_input.text()
        if len(stuid) > 0:
            query_data = {"name":stuid}
            self.execute_query = ExecuteCommand(command='query',data=query_data)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.query_followUp)
    
    def query_followUp(self,response):
        response = json.loads(response)
        if response['status'] == 'OK':
            sys_info =response['parameters']
        else:
            sys_info = "'{}' is not exist".format(self.stuid_input.text())
        self.update_widget("respone")
        self.respone(sys_info)
        
class Respone(QtWidgets.QWidget):
    def __init__(self,update_widget):
        super().__init__()
        self.jump_to_query = update_widget
        layout = QtWidgets.QGridLayout()
        self.show_label = LabelComponent(14, "")
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.show_label)
        scroll.setWidgetResizable(True)
        previous_page = ButtonComponent("上一頁")
        previous_page.clicked.connect(lambda: self.jump_to_query('query'))
        
        layout.addWidget(scroll, 0,0,1,3)
        layout.addWidget(previous_page, 1,1,1,1)
        layout.setColumnStretch(0,4)
        layout.setColumnStretch(1,2)
        layout.setColumnStretch(2,4)
        layout.setRowStretch(0,9)
        layout.setRowStretch(1,1)
        self.setLayout(layout)
    
    def load(self):
        pass
        
    def getInfo(self,parameters):
        sys_info = str(parameters)
        self.show_label.setText(sys_info)