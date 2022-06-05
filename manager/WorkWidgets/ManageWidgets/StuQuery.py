from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent,ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json
class StuQuery(QtWidgets.QWidget):
    def __init__(self,update_widget,getparam):
        super().__init__()
        self.getparam = getparam
        self.jump_to_modify = update_widget
        layout = QtWidgets.QGridLayout()
        
        self.show_label = LabelComponent(20,"")
        stuid_label = LabelComponent(16,"學號:")
        self.stuid_input = LineEditComponent("")
        query = ButtonComponent("查詢")
        query.clicked.connect(self.query_action)
        
        layout.addWidget(stuid_label, 1,1,1,1)
        layout.addWidget(self.stuid_input, 1,2,1,1)
        layout.addWidget(query, 1,3,1,1)
        layout.addWidget(self.show_label, 2,1,1,3)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 3)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 4)
        self.setLayout(layout)
    
    def load(self):
        pass
    
    def query_action(self):
        stuid = self.stuid_input.text()
        if len(stuid) > 0:
            query_data = {'student_id':stuid}
            self.execute_query = ExecuteCommand(command='query_stu_profile',data=query_data)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.query_followUp)
    
    def query_followUp(self,response):
        response = json.loads(response)
        
        if response['status'] == 'OK':
            self.getparam(response['data'])
            self.jump_to_modify('modify')
        else:
            sys_info = "'{}' is not exist".format(self.stuid_input.text())
            self.show_label.setText(sys_info)