from PyQt5 import QtWidgets,QtCore
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from WorkWidgets.SocketClient.ClientControl import ExecuteCommand
import json

class CardAnalyz(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # define the data
        title = "Basic pyqtgraph plot: Bar Graph & xTicks"
        self.plt = pg.PlotWidget()
        self.plt.setWindowTitle(title)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plt)
        self.setLayout(layout)
    
    def load(self):
        self.plt.clear()
        self.QueryData()
        

    
    def QueryData(self):
        now = QtCore.QDateTime.currentDateTime()
        current_datetime = now.toString("yyyy/MM/dd hh:mm:ss")
        past_datetime = now.addDays(-7).toString("yyyy/MM/dd hh:mm:ss")
        date = {'start_time':past_datetime, 'end_time':current_datetime}
        self.execute_query = ExecuteCommand(command='query_logs',data=date)
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.get_info_follwUp)
    
    def get_info_follwUp(self,response):
        days = 7
        date_index = list()
        population_y = [0]*days
        repeat_y = [0]*days
        today = QtCore.QDate.currentDate()
        for i in range(days):
            date = today.addDays(-6+i).toString("MM/dd")
            date_index.append(date)
        response = json.loads(response)
        if response['status'] == 'OK':
            stu_list = list()
            record_list = response['data']
            for student in record_list:
                if student['status'] == 'in':
                    key = student['swipe_time'][5:10]
                    index = date_index.index(key)
                    repeat_y[index]+=1
                    if not student['card_no'] in stu_list:
                        stu_list.append(student['card_no'])
                        population_y[index]+=1
        self.draw_plot(date_index,population_y,repeat_y)
                
    def draw_plot(self,date_index,population_y,repeat_y):
        index_x = list(range(1,len(date_index)+1))
        no_barItem = pg.BarGraphItem(x = index_x, height = population_y, width = 0.2, brush=(107,200,224))
        repeat_barItem = pg.BarGraphItem(x = index_x, y0=population_y,height = repeat_y, width = 0.2, brush=(224,200,107))
        self.plt.addItem(no_barItem)
        self.plt.addItem(repeat_barItem)
        self.plt.getAxis('bottom').setTicks([[(i, date_index[i-1]) for i in index_x]])
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.plt.getAxis("bottom").setStyle(tickFont = font)
        self.plt.getAxis("left").setStyle(tickFont = font)
        self.plt.getAxis("bottom").setTextPen(color='g')
        self.plt.getAxis("bottom").setPen(color='y')
        self.plt.plot()