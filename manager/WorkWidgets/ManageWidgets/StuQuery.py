from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent,LineEditComponent,ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json
class StuQuery(QtWidgets.QWidget):
    def __init__(self,update_widget,getparam):
        super().__init__()
        self.getparam = getparam
        self.jump_to_modify = update_widget
        layout = QtWidgets.QVBoxLayout()
        content_layout =QtWidgets.QHBoxLayout()
        self.show_label = LabelComponent(20,"")
        stuid_label = LabelComponent(16,"School_ID:")
        self.stuid_input = LineEditComponent("")
        search_button = ButtonComponent("")
        search_button.clicked.connect(lambda: self.query_action())
        search_button.setIcon(QtGui.QIcon('./icon/search.png'))
        search_button.setIconSize(QtCore.QSize(30,30))
        
        content_layout.addWidget(stuid_label,alignment=QtCore.Qt.AlignVCenter)
        content_layout.addWidget(self.stuid_input)
        content_layout.addWidget(search_button)
        content_layout.addStretch()
        layout.addLayout(content_layout, 2)
        layout.addWidget(self.show_label, 8)
        self.setLayout(layout)
    
    def load(self):
        self.stuid_input.setText("")
        self.show_label.setText("")
    
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