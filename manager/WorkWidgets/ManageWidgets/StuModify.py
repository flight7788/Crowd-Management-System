from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class StuModify(QtWidgets.QWidget):
    def __init__(self,update_widget):
        super().__init__()
        self.back_query = update_widget
        self.delete_widget = DeleteConfirmWidget(self.delet_confirm)
        self.show_label = LabelComponent(16,"")
        StuId_label = LabelComponent(16,"Student ID")
        self.StuId_input = LineEditComponent("")
        name_label = LabelComponent(16,"Name")
        self.name_input = LineEditComponent("")
        self.name_input.setObjectName("NameLineEdit")
        cardId_label = LabelComponent(16,"Card ID")
        self.cardId_input = LineEditComponent("")
        self.cardId_input.setObjectName("CardIdLineEdit")
        self.modify_botton = ButtonComponent("modify")
        self.delete_botton = ButtonComponent("delete")
        self.cancel_botton = ButtonComponent("cancle")
        self.confirm_botton = ButtonComponent("confirm")
        self.backquery_botton = ButtonComponent("return")
        self.modify_botton.clicked.connect(lambda: self.modify_action())
        self.delete_botton.clicked.connect(lambda: self.delete_action())
        self.cancel_botton.clicked.connect(lambda: self.cancel())
        self.confirm_botton.clicked.connect(lambda: self.confirm_action())
        self.backquery_botton.clicked.connect(lambda: self.back_query('query'))
        self.backquery_botton.setIcon(QtGui.QIcon('./icon/return.png'))
        self.backquery_botton.setIconSize(QtCore.QSize(30,30))
        
        layout = QtWidgets.QVBoxLayout()
        info_layout = QtWidgets.QGridLayout()
        info_layout.addWidget(StuId_label, 0,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        info_layout.addWidget(self.StuId_input, 0,1,1,1)
        info_layout.addWidget(name_label, 1,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        info_layout.addWidget(self.name_input, 1,1,1,1)
        info_layout.addWidget(cardId_label, 2,0,1,1,alignment=QtCore.Qt.AlignVCenter)
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
        function_layout.addWidget(self.backquery_botton, 0,4,1,1)
        function_layout.setColumnStretch(0,2)
        function_layout.setColumnStretch(1,2)
        function_layout.setColumnStretch(2,2)
        function_layout.setColumnStretch(3,2)
        function_layout.setColumnStretch(4,2)
        
        combine_info_show_layout = QtWidgets.QHBoxLayout()
        combine_info_show_layout.addLayout(info_layout)
        combine_info_show_layout.addWidget(self.show_label)
        
        layout.addLayout(combine_info_show_layout)
        layout.addLayout(function_layout)
        layout.addStretch()
        self.setLayout(layout)
    
    def load(self):
        self.name_input.setReadOnly(True)
        self.StuId_input.setReadOnly(True)
        self.cardId_input.setReadOnly(True)
        self.name_input.setStyleSheet("background:rgb(61, 80, 95); color:white;")
        self.StuId_input.setStyleSheet("background:rgb(61, 80, 95); color:white;")
        self.cardId_input.setStyleSheet("background:rgb(61, 80, 95); color:white;")
        self.cancel_botton.hide()
        self.confirm_botton.hide()
        self.modify_botton.show()
        self.delete_botton.show()
        self.backquery_botton.show()
    
    def modify_action(self):
        self.name_input.setReadOnly(False)
        self.cardId_input.setReadOnly(False)
        self.name_input.setStyleSheet("QLineEdit#NameLineEdit{background:rgb(120,120,120); color:black;} QLineEdit:focus#NameLineEdit{background:rgb(220,220,220)};")
        self.cardId_input.setStyleSheet("QLineEdit#CardIdLineEdit{background:rgb(120,120,120); color:black;} QLineEdit:focus#CardIdLineEdit{background:rgb(220,220,220)};")
        self.backquery_botton.hide()
        self.modify_botton.hide()
        self.delete_botton.hide()
        self.cancel_botton.show()
        self.confirm_botton.show()
    
    def delete_action(self):
        self.delete_widget.show_widget()
    
    def delet_confirm(self):
        stuid = {"student_id":self.StuId_input.text()}
        self.execute_delete = ExecuteCommand(command='delete_stu',data=stuid)
        self.execute_delete.start()
        self.execute_delete.return_sig.connect(self.delete_followup)
    
    def delete_followup(self,response):
        response = json.loads(response)
        if response['status'] == 'OK':
            self.back_query("query")
        else:
            warning = response['reason']
            self.show_label.setText(warning)
    
    def confirm_action(self):
        stu_info = {"student_id":self.StuId_input.text(),
                    "card_no":self.cardId_input.text(),
                    "student_name":self.name_input.text()}
        self.execute_confirm = ExecuteCommand(command='modify_stu',data=stu_info)
        self.execute_confirm.start()
        self.execute_confirm.return_sig.connect(self.confirm_followup)
        
    def confirm_followup(self,response):
        response = json.loads(response)
        if response['status'] == 'OK':
            self.load()
        else:
            print("fail")
    
    def cancel(self):
        self.reloadInfo()
        self.load()
    
    def reloadInfo(self):
        self.StuId_input.setText(self.stu_info['student_id'])
        self.name_input.setText(self.stu_info["student_name"])
        self.cardId_input.setText(self.stu_info["card_no"])
        
    def getinfo(self,student):
        self.stu_info = student
        self.reloadInfo()

class DeleteConfirmWidget(QtWidgets.QWidget):
    def __init__(self,callback_delete_confirm):
        super().__init__()
        self.callback_delete_confirm =callback_delete_confirm
        self.setWindowTitle("DeleteConfirm")
        self.setStyleSheet("background-color: rgb(61, 80, 95)")
        warning_label = LabelComponent(12,"Are you sure you want to delete this student?")
        yes_button = ButtonComponent("Yes")
        no_button = ButtonComponent("No")
        yes_button.clicked.connect(lambda: self.button_action('yes'))
        no_button.clicked.connect(lambda: self.button_action('no'))
        
        layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(no_button)
        button_layout.addWidget(yes_button)
        
        layout.addWidget(warning_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def show_widget(self):
        self.show()
        
    def button_action(self,result):
        if result == "yes":
            self.callback_delete_confirm()
        self.close()
        