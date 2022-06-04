import serial
import serial.tools.list_ports
from PyQt5 import QtCore


class CardReader(QtCore.QThread):  
  uid = QtCore.pyqtSignal(str)  

  def __init__(self, parent=None):
    super().__init__(parent)
    self.device = COM()
    self.connect = False

  def run(self):
    while self.connect:
        data = self.device.get_data()
        data = data.decode('UTF-8')
        data = data.strip('\n') 
        data = data.split(':')
        if(len(data) >= 2 and data[0] == 'UID'):
          self.uid.emit(data[1])   
          #print(data[1])

  def open(self, port, baud):
    if(self.connect == False):
      self.device.baud = baud
      self.device.port = port
      self.device.open()
      self.connect = True
      
  def close(self):
      if self.connect:
         self.connect = False
         self.device.close()




class COM:
  def __init__(self, port='', baud=115200):
    self.port = port
    self.baud = int(baud)
    self.open_com = None
    self.get_data_flag = False

  def open(self):
    try:
      self.open_com = serial.Serial(self.port, self.baud)
    except Exception as e:
      print('Open com fail:{}/{}'.format(self.port, self.baud))
      print('Exception:{}'.format(e))

  def close(self):
    if self.open_com is not None and self.open_com.isOpen:
      self.open_com.close()

  def send_data(self, data):
    if self.open_com is None:
      self.open()
    success_bytes = self.open_com.write(data.encode('UTF-8'))
    return success_bytes

  def get_data(self):
    data = self.open_com.readline()
    return data

  def get_list_port(self):
    ports = serial.tools.list_ports.comports(include_links=False)
    return ports



if __name__ == '__main__':
  MyCOM = CardReader()
  for i in MyCOM.device.get_list_port():
    print(i.name, i.description)
  '''
  def callback(data):
    if(data == '30a3557e'):
      MyCOM.device.send_data('Card:PASS\n')
    else:
      MyCOM.device.send_data('Card:FAIL\n')

  MyCOM.uid.connect(callback) 
  MyCOM.open('com6', 115200)
  MyCOM.run()
  '''
  

