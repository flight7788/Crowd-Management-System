from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class StuAdd(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.show_label = LabelComponent(16,"")
        name_label = LabelComponent(14,"Name")
        self.name_input = LineEditComponent("")
        stuid_label = LabelComponent(14,"School_ID")
        self.stuid_input = LineEditComponent("")
        cardid_label = LabelComponent(14,"Card_ID")
        self.cardid_input = LineEditComponent("")
        self.add_button = ButtonComponent("comfire")
        self.add_button.clicked.connect(lambda: self.add())
        
        
        layout = QtWidgets.QHBoxLayout()
        work_layout = QtWidgets.QGridLayout()
        work_layout.addWidget(name_label, 0,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        work_layout.addWidget(self.name_input, 0,1,1,2)
        work_layout.addWidget(stuid_label, 1,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        work_layout.addWidget(self.stuid_input, 1,1,1,2)
        work_layout.addWidget(cardid_label, 2,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        work_layout.addWidget(self.cardid_input, 2,1,1,2)
        work_layout.addWidget(self.add_button, 4,2,1,1)
        work_layout.setColumnStretch(0, 1)
        work_layout.setColumnStretch(1, 8)
        work_layout.setColumnStretch(2, 1)
        work_layout.setRowStretch(0, 2)
        work_layout.setRowStretch(1, 2)
        work_layout.setRowStretch(2, 2)
        work_layout.setRowStretch(3, 2)
        work_layout.setRowStretch(4, 2)
        
        layout.addLayout(work_layout,6)
        layout.addWidget(self.show_label,4)
        self.setLayout(layout)
        
    def load(self):
        self.name_input.setText("")
        self.stuid_input.setText("")
        self.cardid_input.setText("")
        self.show_label.setText("")
        
    def add(self):
        self.add_button.setEnabled(False)
        student_id= self.stuid_input.text()
        card_no = self.cardid_input.text()
        student_name = self.name_input.text()
        if (student_id and card_no and student_name):
            stu_info = {'student_id': student_id,
                        'card_no': card_no,
                        'student_name': student_name}
            self.execute_query = ExecuteCommand(command='add_stu',data=stu_info)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.add_followUp)
        else:
            warning = "There are fields not entered"
            self.show_label.setText(warning)
    
    def add_followUp(self,response):
        response = json.loads(response)
        if response['status'] == 'OK':
            warning = "Add Success"
            self.show_label.setText(warning)
            self.load()
        else:
            warning = "Add Fail\n"+response["reason"]
        self.show_label.setText(warning)
        self.add_button.setEnabled(True)