from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class StuShow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        header_layout = QtWidgets.QHBoxLayout()
        show_label = LabelComponent(16,"show all student")
        self.info_table = table()
        refresh_label = ButtonComponent("refresh")
        refresh_label.setIcon(QtGui.QIcon('./icon/refresh.png'))
        refresh_label.setIconSize(QtCore.QSize(40,40))
        refresh_label.clicked.connect(lambda: self.query())
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.info_table)
        scroll.setWidgetResizable(True)
        self.info_table.setStyleSheet("background-color: rgb(144, 144, 144)")
        
        header_layout.addWidget(show_label)
        header_layout.addWidget(refresh_label)
        header_layout.addStretch()
        layout.addLayout(header_layout,1)
        layout.addWidget(self.info_table,9)
        self.setLayout(layout)
    
    def load(self):
        pass
    
    def query(self):
        self.execute_query = ExecuteCommand(command='query_all_stu',data={})
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.show_followUp)
    
    def show_followUp(self,response):
        self.info_table.refresh()
        response = json.loads(response)
        if response['status'] == 'OK':
            data = response['data']
            for index,student in enumerate(data):
                self.info_table.insertRow(index)
                for index_col,colnum in enumerate(self.info_table.horizontalHeader):
                    self.info_table.setItem(index,index_col,QtWidgets.QTableWidgetItem(student[colnum]))
        
class table(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.horizontalHeader = ['student_id',"student_name","card_no"]
        self.refresh()
        self.setEditTriggers(self.NoEditTriggers)
        self.setColumnWidth(4,200)
        self.setRowHeight(0,40)
        
    def refresh(self):
        self.clear()
        self.setColumnCount(len(self.horizontalHeader))
        self.setHorizontalHeaderLabels(self.horizontalHeader)
        self.setRowCount(0)
