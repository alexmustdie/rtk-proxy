import time
from PyQt5.QtCore import pyqtSignal, QThread

class Checker(QThread):

  sleepTime = 5
  status = pyqtSignal(str)
  terminate = False

  def __init__(self, device):
    QThread.__init__(self)
    self.device = device

  def run(self):

    while not self.terminate:

      try:
        status = self.device['status'].read()[0]
        if status == 0: self.status.emit('Нет связи  с приёмником, приёмник не работает или не подключён')
        elif status == 1: self.status.emit('Приёмник проинициализирован, но нет сигнала от спутников, возможна проблема с антенной или приёмом')
        elif status == 2: self.status.emit('Приёмник получает информацию от спутников')
        elif status == 3: self.status.emit('Приёмнику достаточно данных для расчёта координат и скоростей')
        elif status == 4: self.status.emit('Приёмник получает и использует поправки RTK')
      except:
        pass

      time.sleep(self.sleepTime)
