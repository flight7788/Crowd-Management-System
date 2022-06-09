from PyQt5 import QtWidgets,QtCore,QtGui
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
from WorkWidgets.RecordTapWidgets.ImageProcessor import ImageProcessor
import datetime,os,json

class CardShow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.calendar = CalendarView(self.custom_followUP)
        self.image_widget = ImageWidget()
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
        
    def show_followUp(self,response):
        self.show_table.refresh()
        self.img_button_list = list()
        response = json.loads(response)
        if response['status'] == 'OK':
            record_list = response['data']
            img_binary_list = list()
            for record in record_list:
                img_binary_list.append(record['img_binary'])
            for index,record in enumerate(record_list):
                self.show_table.insertRow(index)
                self.img_button_list.append(ButtonComponent(""))
                self.img_button_list[index].clicked.connect(lambda: self.img_button_action(img_binary_list))
                self.img_button_list[index].setIcon(QtGui.QIcon('./icon/img_detail.png'))
                self.img_button_list[index].setIconSize(QtCore.QSize(30,30))
                self.img_button_list[index].setObjectName("img_button_list {}".format(index))
                self.show_table.setCellWidget(index,0, self.img_button_list[index])
                collist = self.show_table.horizontalHeader
                for index_col,colnum in enumerate(collist):
                    if not index_col == 0:
                        self.show_table.setItem(index,index_col,QtWidgets.QTableWidgetItem(record[colnum]))
        
    def call_back_action(self,parameters):
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
        
    
    def custom_followUP(self,stare_time,end_time):
        self.show_logs(stare_time,end_time)
        
    def img_button_action(self,img_binary_list):
        sending_button = str(self.sender().objectName())
        index =int(sending_button.split()[-1])
        self.query_img_action(img_binary_list[index])
        
    def query_img_action(self,img_binary):
        data = {'file_name':img_binary}
        self.execute_query = ExecuteCommand(command='query_image_binary',data=data)
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.query_img_followUp)
    
    def query_img_followUp(self,response):
        response_ = json.loads(response)
        print(type(response_))
        self.image_widget.decode_image(response_["data"])
        
        
class ImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Picture")
        layout = QtWidgets.QVBoxLayout()
        self.image_label = LabelComponent(12,"")
        layout.addWidget(self.image_label)
        self.setLayout(layout)
    
    def decode_image(self,image):
        self.decode = ImageProcessor(image)
        self.decode.start()
        self.decode.return_sig.connect(self.show_image)
    
    def show_image(self,picture):
        self.picture = picture
        pixmap = QtGui.QPixmap(picture)
        self.image_label.setPixmap(pixmap)
        self.show()
        
    def closeEvent(self, event):
        event.accept()
        os.remove(self.picture)

class showtable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.horizontalHeader = ["img_binary","card_no","swipe_time","status","client_no"]
        self.refresh()
        self.setEditTriggers(self.NoEditTriggers)
        self.setStyleSheet("""QTableWidget::item{color:white};
                                        font: bold 10px;
                                        background-color: rgb(33, 43, 51)""")
        
    def refresh(self):
        self.clear()
        self.setColumnCount(len(self.horizontalHeader))
        self.setHorizontalHeaderLabels(self.horizontalHeader)
        self.setColumnWidth(0, 50)
        self.setRowCount(0)
        
class CalendarView(QtWidgets.QWidget):
    def __init__(self,call_back_time):
        super().__init__()
        self.StartClicked = True
        self.EndClicked = False
        self.date =""
        self.call_back_time = call_back_time
        self.setWindowTitle('Calendar')
        
        low_date = QtCore.QDate(2022, 1, 1)
        up_date = QtCore.QDate.currentDate()
        calendar = QtWidgets.QCalendarWidget(self)
        calendar.setDateRange(low_date, up_date)
        calendar.setGridVisible(True)
        calendar.move(20, 20)
        calendar.clicked[QtCore.QDate].connect(self.GetDate)        

        start_label = LabelComponent(10,"start time:")
        end_label = LabelComponent(10,"end time:")
        self.get_start_lineEdit = LineEditComponent("",font_size=10)
        self.get_end_lineEdit = LineEditComponent("",font_size=10)
        self.get_start_lineEdit.mousePressEvent = self.GetStartDate
        self.get_end_lineEdit.mousePressEvent = self.GetEndDate
        self.start_time_edit = QtWidgets.QTimeEdit()
        self.end_time_edit = QtWidgets.QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        self.start_time_edit.setTime(QtCore.QTime.currentTime())
        self.end_time_edit.setTime(QtCore.QTime.currentTime())
        confirm_button = ButtonComponent("confirm",font_size=8)
        confirm_button.clicked.connect(self.DateProcessing)
        self.show_label = LabelComponent(12,"")
        
        start_label.setStyleSheet("color: black")
        end_label.setStyleSheet("color: black")
        self.show_label.setStyleSheet("color: red")
        self.get_start_lineEdit.setStyleSheet("color: black")
        self.get_end_lineEdit.setStyleSheet("color: black")
        confirm_button.setStyleSheet("color: black")
        
        layout = QtWidgets.QVBoxLayout()
        contents_layout = QtWidgets.QGridLayout()
        confirm_layout = QtWidgets.QHBoxLayout()
        
        contents_layout.addWidget(start_label,0,0,1,1)
        contents_layout.addWidget(end_label,1,0,1,1)
        contents_layout.addWidget(self.get_start_lineEdit,0,1,1,1)
        contents_layout.addWidget(self.get_end_lineEdit,1,1,1,1)
        contents_layout.addWidget(self.start_time_edit,0,2,1,1)
        contents_layout.addWidget(self.end_time_edit,1,2,1,1)
        
        confirm_layout.addWidget(self.show_label,9)
        confirm_layout.addWidget(confirm_button,1)
        
        layout.addWidget(calendar)
        layout.addLayout(contents_layout)
        layout.addLayout(confirm_layout)
        self.setLayout(layout)
        
    def showcalendar(self):
        currentDate = QtCore.QDate.currentDate().toString("yyyy/MM/dd")
        self.get_start_lineEdit.setText("")
        self.get_end_lineEdit.setText(currentDate)
        self.end_time_edit.setTime(QtCore.QTime.currentTime())
        
        self.show()
    
    def GetDate(self, date):
        self.date = date.toString("yyyy/MM/dd")
        if self.StartClicked:
            self.get_start_lineEdit.setText(self.date)
        else:
            self.get_end_lineEdit.setText(self.date)
    
    def GetStartDate(self, event):
        self.StartClicked = True
        
    def GetEndDate(self, event):
        self.StartClicked = False
    
    def DateProcessing(self):
        warning = ""
        start_date = self.get_start_lineEdit.text()
        end_date = self.get_end_lineEdit.text()
        if not start_date:
            warning = "start_time didn't select"
        if not end_date:
            warning = "end_time didn't select"
        if start_date and end_date:
            start_time = self.start_time_edit.time().toString("hh:mm:ss")
            end_time = self.end_time_edit.time().toString("hh:mm:ss")
            start_datetime = start_date+" "+start_time
            end_datetime = end_date+" "+end_time
            date_start = datetime.datetime.strptime(start_datetime, '%Y/%m/%d %H:%M:%S')
            date_end = datetime.datetime.strptime(end_datetime, '%Y/%m/%d %H:%M:%S')
            if date_start<date_end:
                self.SentDate(start_datetime,end_datetime)
            else:
                warning = "The start time must be earlier than the end time"
        self.show_label.setText(warning)
            
            
        
    def SentDate(self,StartTime,EndTime):
        self.call_back_time(StartTime,EndTime)
        self.hide()