import sys

from serial import Serial
from logic import proto, Input

class BaseStation:

  class Thread(Input.Thread):

    def __init__(self, baseStationOptions, outputClientStream):

      super().__init__()

      self.inputClient = BaseStation.Client(**baseStationOptions)
      self.connectOutputClient(outputClientStream)

  class Client(Input.Client):

    def __init__(self, serial, baudrate):

      super().__init__()

      self.conn = Serial()
      self.conn.port = serial
      self.conn.baudrate = baudrate
      self.conn.parity = 'N'
      self.conn.rtscts = False
      self.conn.xonxoff = False
      self.conn.timeout = 0.01
      self.version = sys.version_info[0]

      try:
        self.conn.open()
      except:
        raise Exception('Could not open serial port ' + self.conn.portstr)

    def readData(self, hub):

      bytesCount = 0
      self.bytesCount.emit(bytesCount)

      while not self.terminate:

        try:
          response = self.conn.read(256)
        except serial.SerialException:
          raise Exception('Serial port error')

        while len(response) > 0:

          length = min(len(response), 32)
          chunk = response[:length]
          response = response[length:]

          bytesCount += sys.getsizeof(chunk)
          self.bytesCount.emit(bytesCount)
          
          # print(chunk)

          packet = {'id': proto.Message.COMPONENT_RAW_DATA, 'component': self.device.address, 'payload': chunk}
          hub.messenger.invokeAsync(packet = packet, callback = None)

      self.bytesCount.emit(0)
      self.conn.close()
