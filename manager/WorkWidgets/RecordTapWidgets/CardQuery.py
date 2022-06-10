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
        layout = QtWidgets.QVBoxLayout()
        query_layout = QtWidgets.QHBoxLayout()
        
        self.show_label = LabelComponent(16,"")
        stuid_label = LabelComponent(16,"Student ID:")
        self.stuid_input = LineEditComponent("")
        query_button = ButtonComponent("")
        query_button.setIcon(QtGui.QIcon('./icon/search.png'))
        query_button.setIconSize(QtCore.QSize(20,20))
        query_button.clicked.connect(self.query_action)
        
        query_layout.addWidget(stuid_label,alignment=QtCore.Qt.AlignVCenter)
        query_layout.addWidget(self.stuid_input)
        query_layout.addWidget(query_button)
        query_layout.addStretch()
        
        layout.addLayout(query_layout)
        layout.addWidget(self.show_label)
        self.setLayout(layout)
    
    def load(self):
        self.stuid_input.setText("")
        self.show_label.setText("")
    
    def query_action(self):
        stuid = self.stuid_input.text()
        if len(stuid) > 0:
            query_data = {"student_id":stuid}
            self.execute_query = ExecuteCommand(command='query_stu',data=query_data)
            self.execute_query.start()
            self.execute_query.return_sig.connect(self.query_followUp)
    
    def query_followUp(self,response):
        response = json.loads(response)
        warning = ""
        if response['status'] == 'OK':
            self.respone_callback(json.dumps(response))
            self.update_widget('show')
        else:
            warning = "student {} have no info".format(self.stuid_input.text())
            self.show_label.setText(warning)