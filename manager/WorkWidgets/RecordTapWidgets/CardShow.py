from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class CardShow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")
        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(20, "Show Student")
        self.show_label = LabelComponent(14, "")
        scroll = QtWidgets.QScrollArea()

        scroll.setWidget(self.show_label)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(scroll,stretch=9)
        self.setLayout(layout)
    
    def load(self):
        self.execute_query = ExecuteCommand(command='show',data={})
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.show_followUp)
        
    def show_followUp(self,response):
        sys_info = ""
        response = json.loads(response)
        if response['status'] == 'OK':
            student_list = response['parameter']
            sys_info +="\n  ==== student list ====\n"
            for students in student_list:
                sys_info +="    Name:{}\n".format(students['name'])
                for subject, score in students['scores'].items():
                    sys_info +="        subject: {}, score: {}\n".format(subject,score)
            sys_info +="\n  ======================\n"
        else:
            sys_info = "Show is fail"
        self.show_label.setText(sys_info)
