from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class CardShow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")
        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(20, "Show Record")
        self.show_table = showtable()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.show_table)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(scroll,stretch=9)
        self.setLayout(layout)
    
    def load(self):
        date = {'start_time': '2022/06/01 00:00:00', 'end_time': '2022/06/30 23:59:59'}
        self.execute_query = ExecuteCommand(command='query_logs',data=date)
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.show_followUp)
        
    def show_followUp(self,response):
        self.show_table.refresh()
        response = json.loads(response)
        if response['status'] == 'OK':
            record_list = response['data']
            for index,record in enumerate(record_list):
                print(index,record)
                self.show_table.insertRow(index)
                for index_col,colnum in enumerate(self.show_table.horizontalHeader):
                    self.show_table.setItem(index,index_col,QtWidgets.QTableWidgetItem(record[colnum]))
        
class showtable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.horizontalHeader = ["img_binary","card_no","swipe_time","status","client_no"]
        self.refresh()
        self.setEditTriggers(self.NoEditTriggers)
        self.setColumnWidth(4,200)
        self.setRowHeight(0,40)
        
    def refresh(self):
        self.clear()
        self.setColumnCount(len(self.horizontalHeader))
        self.setHorizontalHeaderLabels(self.horizontalHeader)
        self.setRowCount(0)
