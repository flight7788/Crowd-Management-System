from PyQt5 import QtWidgets,QtCore,QtGui
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class CardShow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.calendar = ShortDatetimeEdit()
        layout = QtWidgets.QVBoxLayout()
        functiom_layout = QtWidgets.QHBoxLayout()
        one_day_button = ButtonComponent("past day")
        one_week_button = ButtonComponent("past week")
        custom_button = ButtonComponent("custom")
        one_day_button.clicked.connect(lambda: self.past_day_action())
        one_week_button.clicked.connect(lambda: self.past_week_action())
        custom_button.clicked.connect(lambda: self.custom_action())
        
        functiom_layout.addWidget(one_day_button)
        functiom_layout.addWidget(one_week_button)
        functiom_layout.addWidget(custom_button)
        
        self.show_table = showtable()
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.show_table)
        scroll.setWidgetResizable(True)
        
        layout.addLayout(functiom_layout, stretch=1)
        layout.addWidget(scroll,stretch=9)
        self.setLayout(layout)
    
    def load(self):
        self.past_day_action()
    
    def show_logs(self,start_time,end_time):
        date = {'start_time': start_time, 'end_time': end_time}
        self.execute_query = ExecuteCommand(command='query_logs',data=date)
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.show_followUp)
        self.mod = "all_stu"
        
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
    
    def call_back_action(self,parameters):
        self.mod = "personal"
        self.show_followUp(parameters)
       
    def past_day_action(self):
        now = QtCore.QDateTime.currentDateTime()
        current_datetime = now.toString("yyyy/MM/dd hh:mm:ss")
        past_datetime =current_datetime.split()
        past_datetime = past_datetime[0] + " 00:00:00"
        self.show_logs(past_datetime,current_datetime)
            
    def past_week_action(self):
        now = QtCore.QDateTime.currentDateTime()
        current_datetime = now.toString("yyyy/MM/dd hh:mm:ss")
        past_datetime = now.addDays(-7).toString("yyyy/MM/dd hh:mm:ss")
        self.show_logs(past_datetime,current_datetime)
    
    def custom_action(self):
        self.calendar.showcalendar()
        now = QtCore.QDateTime.currentDateTime()
        current_datetime = now.toString("yyyy/MM/dd hh:mm:ss")
        past_datetime = now.addDays(-7).toString("yyyy/MM/dd hh:mm:ss")
        self.show_logs(past_datetime,current_datetime)

class showtable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.horizontalHeader = ["img_binary","card_no","swipe_time","status","client_no"]
        self.refresh()
        self.setEditTriggers(self.NoEditTriggers)
        self.setStyleSheet("""QTableWidget::item{color:white};
                                        font: bold 10px;
                                        background-color: rgb(144, 144, 144)""")
        
    def refresh(self):
        self.clear()
        self.setColumnCount(len(self.horizontalHeader))
        self.setHorizontalHeaderLabels(self.horizontalHeader)
        self.setRowCount(0)
        
class ShortDatetimeEdit(QtWidgets.QWidget):
    def __init__(self):
        super(ShortDatetimeEdit, self).__init__()
        
        calendar = QtWidgets.QCalendarWidget(self)
        calendar.setGridVisible(True)
        calendar.move(20, 20)
        calendar.clicked[QtCore.QDate].connect(self.showDate)

        start_label = LabelComponent(12,"start time:")
        end_label = LabelComponent(12,"end time:")
        get_start_label = LabelComponent(12,"")
        get_end_label = LabelComponent(12,"")
        start_confirm_button = ButtonComponent("confirm")
        end_confirm_button = ButtonComponent("confirm")
        contents_layout = QtWidgets.QGridLayout()
        contents_layout.addWidget(start_label,0,0,1,1)
        contents_layout.addWidget(end_label,1,0,1,1)
        contents_layout.addWidget(get_start_label,0,1,1,1)
        contents_layout.addWidget(get_end_label,1,1,1,1)
        contents_layout.addWidget(start_confirm_button,0,2,1,1)
        contents_layout.addWidget(end_confirm_button,1,2,1,1)
        contents_layout.setColumnStretch(0,1)
        contents_layout.setColumnStretch(0,3)
        contents_layout.setColumnStretch(0,1)
        calendar.layout().addChildLayout(contents_layout)

        self.setGeometry(100,100,300,300)
        self.setWindowTitle('Calendar')
        
    def showcalendar(self):
        self.show()
    
    def showDate(self, date):
        self.date = date.toString()       