from PyQt5.QtCore import pyqtSignal, QThread, QObject
from proxy import proto, DeviceStatus

class Thread(QThread):

  inputClient = None
  outputClient = None

  deviceStatus = pyqtSignal(str)
  bytesCount = pyqtSignal(int)
  failed = pyqtSignal(Exception)

  def __init__(self):
    QThread.__init__(self)

  def connectOutputClient(self, outputClientOptions):

    stream = proto.SerialStream(outputClientOptions['serial'], outputClientOptions['baudrate'])

    self.outputClient = proto.Messenger(stream, 'cache')

    self.outputClient.failed.connect(self.raiseException)
    self.outputClient.handler.failed.connect(self.raiseException)

    self.outputClient.connect()

    device = self.outputClient.hub[outputClientOptions['device']]

    if device:
      self.inputClient.device = device
    else:
      self.outputClient.stop()
      raise Exception('Ublox not found')

  def runDeviceStatusChecker(self):
    self.deviceStatusChecker = DeviceStatus.Checker(self.inputClient.device)
    self.deviceStatusChecker.status.connect(self.sendDeviceStatus)
    self.deviceStatusChecker.start()

  def sendDeviceStatus(self, status):
    self.deviceStatus.emit(status)

  def sendBytesCount(self, bytesCount):
    self.bytesCount.emit(bytesCount)

  def raiseException(self, exception):
    self.kill()
    self.failed.emit(exception)

  def run(self):
    try:
      self.runDeviceStatusChecker()
      self.inputClient.bytesCount.connect(self.sendBytesCount)
      self.inputClient.readData(self.outputClient.hub)
    except Exception as exception:
      self.raiseException(exception)

  def kill(self):
    self.deviceStatusChecker.terminate = True
    self.inputClient.terminate = True
    self.outputClient.stop()
    self = None

class Client(QObject):

  terminate = False
  bytesCount = pyqtSignal(int)

  def __init__(self):
    QObject.__init__(self)