from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class StuAdd(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        
        name_label = LabelComponent(16,"姓名")
        self.name_input = LineEditComponent("")
        stuid_label = LabelComponent(16,"學號")
        self.stuid_input = LineEditComponent("")
        cardid_label = LabelComponent(16,"卡號")
        self.cardid_input = LineEditComponent("")
        self.add_botton = ButtonComponent("新增")
        self.add_botton.clicked.connect(lambda: self.add())
        
        layout.addWidget(name_label, 0,1,1,1)
        layout.addWidget(self.name_input, 0,2,1,2)
        layout.addWidget(stuid_label, 1,1,1,1)
        layout.addWidget(self.stuid_input, 1,2,1,2)
        layout.addWidget(cardid_label, 2,1,1,1)
        layout.addWidget(self.cardid_input, 2,2,1,2)
        layout.addWidget(self.add_botton, 3,4,1,1)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)
        layout.setColumnStretch(5, 3)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 2)
        self.setLayout(layout)
        
    def load(self):
        self.name_input.setText("")
        self.stuid_input.setText("")
        self.cardid_input.setText("")
    
    def add(self):
        stu_info = {'student_id': self.stuid_input.text(),
                    'card_no': self.cardid_input.text(),
                    'student_name': self.name_input.text()}
        self.execute_query = ExecuteCommand(command='add_stu',data=stu_info)
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.add_followUp)
    
    def add_followUp(self,response):
        response = json.loads(response)
        if response['status'] == 'OK':
            self.load()
        else:
            pass