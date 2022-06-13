from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class StuShow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.info_table = table()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.info_table)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.setLayout(layout)
        self.refresh()
    
    def load(self):
        pass
    
    def refresh(self):
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
                for index_col,colnum in enumerate(self.info_table.horizontal_list):
                    self.info_table.setItem(index,index_col,QtWidgets.QTableWidgetItem(student[colnum]))
        
class table(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.horizontal_list = ['id',"name","card_no"]
        self.refresh()
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(self.NoEditTriggers)
        self.setStyleSheet("""QTableWidget::item{color:white};
                                        font: bold 10px;
                                        background-color: rgb(144, 144, 144)""")
    def refresh(self):
        self.clear()
        self.setColumnCount(len(self.horizontal_list))
        self.setHorizontalHeaderLabels(['Id',"Name","Card IP"])
        self.setRowCount(0)
