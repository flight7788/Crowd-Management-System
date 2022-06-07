from inspect import Parameter
from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class CardQuery(QtWidgets.QWidget):
    def __init__(self,update_widget,respone_callback):
        super().__init__()
        self.update_widget = update_widget
        self.respone_callback = respone_callback
        layout = QtWidgets.QHBoxLayout()
        
        stuid_label = LabelComponent(16,"學號:")
        self.stuid_input = LineEditComponent("")
        query_button = ButtonComponent("查詢")
        query_button.clicked.connect(self.query_action)
        
        layout.addWidget(stuid_label)
        layout.addWidget(self.stuid_input)
        layout.addWidget(query_button)
        layout.addStretch()
        self.setLayout(layout)
    
    def load(self):
        self.stuid_input.setText("")
    
    def query_action(self):
        stuid = self.stuid_input.text()
        if len(stuid) > 0:
            query_data = {"student_id":stuid}
            self.execute_query = ExecuteCommand(command='query_stu',data=query_data)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.query_followUp)
    
    def query_followUp(self,response):
        response = json.loads(response)
        if response['status'] == 'OK':
            self.respone_callback(json.dumps(response))
            self.update_widget('show')