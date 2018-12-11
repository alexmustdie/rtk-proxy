from logic import proto

class Autopilot:

  def __init__(self, serial, baudrate, device):
    self.serial = serial
    self.baudrate = baudrate
    self.device = device

  def getStream(self):
    return proto.SerialStream(self.serial, self.baudrate)

class Modem:

  def __init__(self, address, port, modemAddress, modemPort, device):
    self.address = address
    self.port = port
    self.modemAddress = modemAddress
    self.modemPort = modemPort
    self.device = device

  def getStream(self):
    return proto.NetworkStream(self.address, self.port, self.modemAddress, self.modemPort)
