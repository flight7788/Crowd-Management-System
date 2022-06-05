from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class StuModify(QtWidgets.QWidget):
    def __init__(self,update_widget):
        super().__init__()
        self.back_query = update_widget
        layout = QtWidgets.QVBoxLayout()
        self.StuId_input =""
        name_label = LabelComponent(16,"姓名")
        self.name_input = LineEditComponent("")
        StuId_label = LabelComponent(16,"學號")
        self.StuId_input = LineEditComponent("")
        cardId_label = LabelComponent(16,"卡號")
        self.cardId_input = LineEditComponent("")
        self.modify_botton = ButtonComponent("修改")
        self.delete_botton = ButtonComponent("刪除")
        self.cancel_botton = ButtonComponent("取消")
        self.confirm_botton = ButtonComponent("確定")
        self.backquery_botton = ButtonComponent("返回")
        self.modify_botton.clicked.connect(lambda: self.modify_action())
        self.delete_botton.clicked.connect(lambda: self.delete_action())
        self.cancel_botton.clicked.connect(lambda: self.cancel())
        self.confirm_botton.clicked.connect(lambda: self.confirm_action())
        self.backquery_botton.clicked.connect(lambda: self.back_query('query'))
        
        info_layout = QtWidgets.QGridLayout()
        info_layout.addWidget(name_label, 0,0,1,1)
        info_layout.addWidget(self.name_input, 0,1,1,1)
        info_layout.addWidget(StuId_label, 1,0,1,1)
        info_layout.addWidget(self.StuId_input, 1,1,1,1)
        info_layout.addWidget(cardId_label, 2,0,1,1)
        info_layout.addWidget(self.cardId_input, 2,1,1,1)
        info_layout.setColumnStretch(0,1)
        info_layout.setColumnStretch(1,5)
        info_layout.setColumnStretch(2,3)
        info_layout.setRowStretch(0,3)
        info_layout.setRowStretch(1,3)
        info_layout.setRowStretch(2,3)
        info_layout.setRowStretch(3,1)
        function_layout = QtWidgets.QGridLayout()
        function_layout.addWidget(self.cancel_botton, 0,1,1,1)
        function_layout.addWidget(self.confirm_botton, 0,2,1,1)
        function_layout.addWidget(self.modify_botton, 0,1,1,1)
        function_layout.addWidget(self.delete_botton, 0,2,1,1)
        function_layout.addWidget(self.backquery_botton, 0,3,1,1)
        function_layout.setColumnStretch(0,2)
        function_layout.setColumnStretch(1,2)
        function_layout.setColumnStretch(2,2)
        function_layout.setColumnStretch(3,2)
        function_layout.setColumnStretch(4,2)
        self.cancel()
        
        layout.addLayout(info_layout)
        layout.addLayout(function_layout)
        self.setLayout(layout)
    
    def load(self):
        self.cancel()
    
    def cancel(self):
        self.name_input.setReadOnly(True)
        self.StuId_input.setReadOnly(True)
        self.cardId_input.setReadOnly(True)
        self.cancel_botton.hide()
        self.confirm_botton.hide()
        self.modify_botton.show()
        self.delete_botton.show()
    
    def modify_action(self):
        self.name_input.setReadOnly(False)
        self.StuId_input.setReadOnly(False)
        self.cardId_input.setReadOnly(False)
        self.modify_botton.hide()
        self.delete_botton.hide()
        self.cancel_botton.show()
        self.confirm_botton.show()
    
    def delete_action(self):
        stuid = {"student_id":self.StuId_input}
        self.execute_delete = ExecuteCommand(command='delete_stu',data=stuid)
        self.execute_delete.start()
        self.execute_delete.return_sig.connect(self.delete_followUp)
    
    def delete_followup(self):
        response = json.loads(response)
        if response['status'] == 'OK':
            pass
        else:
            pass
    
    def confirm_action(self):
        stu_info = {"student_id":self.StuId_input.text(),
                    "card_no":self.cardId_input.text(),
                    "student_name":self.name_input.text()}
        self.execute_confirm = ExecuteCommand(command='modify',data=stu_info)
        self.execute_confirm.start()
        self.execute_confirm.return_sig.connect(self.confirm_followUp)
        
    def confirm_followup(self):
        response = json.loads(response)
        if response['status'] == 'OK':
            pass
        else:
            pass
    
    def getinfo(self,student):
        self.StuId_input.setText(student['student_id'])
        self.name_input.setText(student["student_name"])
        self.cardId_input.setText(student["card_no"])