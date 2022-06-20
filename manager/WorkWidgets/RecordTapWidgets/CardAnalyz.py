from PyQt5 import QtWidgets,QtCore
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui
from SocketClient.ClientControl import ExecuteCommand
from PyQt5.QtWidgets import QWidget
import json

class CardAnalyz(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.graph = GraphWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.graph.plt)
        self.setLayout(layout)
    
    def load(self):
        self.graph.plt.clear()
        self.QueryData()
        
    
    def QueryData(self):
        now = QtCore.QDateTime.currentDateTime()
        current_datetime = now.toString("yyyy/MM/dd hh:mm:ss")
        past_datetime = now.addDays(-7).toString("yyyy/MM/dd hh:mm:ss")
        date = {'start_time':past_datetime, 'end_time':current_datetime}
        self.execute_query = ExecuteCommand(command='query_logs_by_time',data=date)
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.get_info_follwUp)
    
    def get_info_follwUp(self,response):
        days = 7
        date_index = list()
        in_count = [0]*days
        out_count = [0]*days
        today = QtCore.QDate.currentDate()
        for i in range(days):
            date = today.addDays(-days+1+i).toString("MM/dd")
            date_index.append(date)
            print(i,date)
        
        response = json.loads(response)
        if response['status'] == 'OK':
            record_list = response['data']
            for student in record_list:
                key = student['time'][5:10]
                if key in date_index:
                    index = date_index.index(key)
                    if student['action'] == 'in':
                        in_count[index]+=1
                    elif student['action'] == 'out':
                        out_count[index]+=1
        self.graph.draw_plot(date_index,in_count,out_count)
                

class GraphWidget():
    def __init__(self):
        self.plt = pg.plot()
        self.plt.setTitle('Flow of people',**{'size': '18pt'})
        self.plt.addLegend(offset=(5,5))
        
        
    def draw_plot(self,date_index,in_count,out_count):
        index_x = np.arange(7)
        out_count_barItem = pg.BarGraphItem(x = index_x-0.11, height = out_count, width = 0.2, brush=(107,200,224), name='Out Times')
        in_count_barItem = pg.BarGraphItem(x = index_x+0.11,height = in_count, width = 0.2, brush=(224,200,107), name='In Times')
        self.plt.addItem(out_count_barItem)
        self.plt.addItem(in_count_barItem)
        self.plt.getAxis('bottom').setTicks([[(i, date_index[i]) for i in range(0,7)]])
        
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.plt.getAxis("bottom").setStyle(tickFont = font)
        self.plt.getAxis("left").setStyle(tickFont = font)
        self.plt.setLabel('left', "Frequency")
        self.plt.setLabel('bottom',"Date")
        self.plt.getAxis("bottom").setTextPen(color='g')
        self.plt.getAxis("bottom").setPen(color='y')
        self.plt.plot()