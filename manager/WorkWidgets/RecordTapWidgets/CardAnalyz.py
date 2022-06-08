from PyQt5 import QtWidgets,QtCore
from cv2 import addWeighted
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
        population_y = [10, 30, 20]
        date_name = ["A","B","C"]
        response = json.loads(response)
        if response['status'] == 'OK':
            stu_list = list()
            timedict = dict()
            population_y = list()
            date_name = list()
            record_list = response['data']
            for student in record_list:
                if student['status'] == 'in':
                    if not student['card_no'] in stu_list:
                        stu_list.append(student['card_no'])
                        key = student['swipe_time'][5:10]
                        if key in timedict.keys():
                            timedict[key]+=1
                        else:
                            timedict[key] = 1
            for k, v in timedict.items():
                date_name.append(k)
                population_y.append(v)
        
        index_x = list(range(1,len(date_name)+1))
        barItem = pg.BarGraphItem(x = index_x, height = population_y, width = 0.3, brush=(107,200,224))
        self.plt.addItem(barItem)
        
        self.plt.getAxis('bottom').setTicks([[(i, date_name[i-1]) for i in index_x]])
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.plt.getAxis("bottom").setStyle(tickFont = font)
        self.plt.getAxis("left").setStyle(tickFont = font)
        self.plt.getAxis("bottom").setTextPen(color='g')
        self.plt.getAxis("bottom").setPen(color='y')
        self.plt.plot()