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
        self.name_input.setObjectName("nameLineEdit")
        self.name_input.setStyleSheet("QLineEdit#nameLineEdit{color:white} QLineEdit:focus#nameLineEdit{background:rgb(150,150,150); color:white}")
        id_label = LabelComponent(14,"ID")
        self.id_input = LineEditComponent("")
        self.id_input.setObjectName("idLineEdit")
        self.id_input.setStyleSheet("QLineEdit#idLineEdit{color:white} QLineEdit:focus#idLineEdit{background:rgb(150,150,150); color:white}")
        cardid_label = LabelComponent(14,"Card ID")
        self.cardid_input = LineEditComponent("")
        self.cardid_input.setObjectName("cardidLineEdit")
        self.cardid_input.setStyleSheet("QLineEdit#cardidLineEdit{color:white} QLineEdit:focus#cardidLineEdit{background:rgb(150,150,150); color:white}")
        self.add_button = ButtonComponent("Confirm")
        self.add_button.clicked.connect(lambda: self.add())
        self.add_button.setObjectName('add_button')
        self.add_button.setStyleSheet("""
            QPushButton#add_button{
                border: 2px solid rgb(255, 255, 255);
                border-radius: 10px;
                color: white;
            }
            
            QPushButton#add_button:hover {
                background-color: rgb(200, 200, 200);
                color: black;
            }
        """)

        layout = QtWidgets.QHBoxLayout()
        work_layout = QtWidgets.QGridLayout()
        work_layout.addWidget(id_label, 0,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        work_layout.addWidget(self.id_input, 0,1,1,2)
        work_layout.addWidget(name_label, 1,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        work_layout.addWidget(self.name_input, 1,1,1,2)
        work_layout.addWidget(cardid_label, 2,0,1,1,alignment=QtCore.Qt.AlignVCenter)
        work_layout.addWidget(self.cardid_input, 2,1,1,2)
        work_layout.addWidget(self.add_button, 3,0,1,1)
        work_layout.setColumnStretch(0, 3)
        work_layout.setColumnStretch(1, 7)
        work_layout.setRowStretch(0, 2)
        work_layout.setRowStretch(1, 2)
        work_layout.setRowStretch(2, 2)
        work_layout.setRowStretch(3, 2)
        work_layout.setRowStretch(4, 2)
        
        layout.addLayout(work_layout,7)
        layout.addWidget(self.show_label,3)
        self.setLayout(layout)
        
    def load(self):
        self.name_input.setText("")
        self.id_input.setText("")
        self.cardid_input.setText("")
        self.show_label.setText("")
        
    def add(self):
        self.add_button.setEnabled(False)
        id= self.id_input.text()
        card_no = self.cardid_input.text()
        name = self.name_input.text()
        if (id and card_no and name):
            stu_info = {'id': id,
                        'name': name,
                        'card_no': card_no}
            self.execute_query = ExecuteCommand(command='add_stu',data=stu_info)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.add_followUp)
        else:
            warning = "There are fields not entered"
            self.show_label.setText(warning)
            self.add_button.setEnabled(True)
    
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