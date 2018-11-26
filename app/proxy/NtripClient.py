import socket
import datetime
import base64
import time

from PyQt5.QtCore import pyqtSignal, QThread, QObject
from proxy import proto

class DeviceStatusHandler(QThread):

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
      except:
        pass
        
      if status == 0: self.status.emit('Нет связи  с приёмником, приёмник не работает или не подключён')
      elif status == 1: self.status.emit('Приёмник проинициализирован, но нет сигнала от спутников')
      elif status == 2: self.status.emit('Приёмник получает информацию от спутников')
      elif status == 3: self.status.emit('Приёмнику достаточно данных для расчёта координат и скоростей')
      elif status == 4: self.status.emit('Приёмник получает и использует поправки RTK')

      time.sleep(self.sleepTime)

class NtripClientThread(QThread):

  client = None
  messenger = None

  deviceStatus = pyqtSignal(str)
  progress = pyqtSignal(int)
  failed = pyqtSignal(str)

  def __init__(self, ntripOptions, autopilotOptions):

    QThread.__init__(self)

    if ntripOptions['mountpoint'][0:1] != '/':
      ntripOptions['mountpoint'] = '/' + ntripOptions['mountpoint']

    ntripOptions['lat'] = 50.09
    ntripOptions['lon'] = 8.66
    ntripOptions['height'] = 1200
    ntripOptions['verbose'] = True

    if ntripOptions['verbose']:
      print('server: ' + ntripOptions['server'])
      print('port: ' + str(ntripOptions['port']))
      print('user: ' + ntripOptions['user'])
      print('mountpoint: ' + ntripOptions['mountpoint'])
      print('serial: ' + autopilotOptions['serial'])
      print('baudrate: ' + autopilotOptions['baudrate'])
      print('device: ' + autopilotOptions['device'])
      print()

    stream = proto.SerialStream(autopilotOptions['serial'], autopilotOptions['baudrate'])

    self.messenger = proto.Messenger(stream, 'cache')
    self.messenger.connect()

    proto.verboseEnabled = False

    device = self.messenger.hub[autopilotOptions['device']]

    if device:
      self.client = NtripClient(**ntripOptions)
      self.client.setDevice(device)
    else:
      self.messenger.stop()
      raise Exception('Ublox not found')

  def sendDeviceStatus(self, status):
    self.deviceStatus.emit(status)

  def sendProgress(self, progress):
    self.progress.emit(progress)

  def run(self):

    self.deviceStatusHandler = DeviceStatusHandler(self.client.device)
    self.deviceStatusHandler.start()
    self.deviceStatusHandler.status.connect(self.sendDeviceStatus)

    try:
      self.client.progress.connect(self.sendProgress)
      self.client.readData(self.messenger.hub)
    except Exception as exception:
      self.failed.emit(str(exception))

  def kill(self):
    self.deviceStatusHandler.terminate = True
    self.client.terminate = True
    self.messenger.stop()

class NtripClient(QObject):

  terminate = False
  progress = pyqtSignal(int)

  def __init__(self,
     buffer = 50,
     user = '',
     password = '',
     port = 2101,
     server = '',
     mountpoint = '',
     lat = 46,
     lon = 122,
     height = 1212,
     verbose = False):

    QObject.__init__(self)

    self.buffer = buffer
    self.user = base64.b64encode((user + ':' + password).encode()).decode()
    self.port = int(port)
    self.server = server
    self.mountpoint = mountpoint
    self.setPosition(lat, lon)
    self.height = height
    self.verbose = verbose

  def setDevice(self, device):
    self.device = device

  def setPosition(self, lat, lon):

    self.flagN = 'N'
    self.flagE = 'E'

    if lon > 180:
      lon = (lon - 360) *- 1
      self.flagE = 'W'
    elif (lon < 0 and lon >= -180):
      lon = lon *- 1
      self.flagE = 'W'
    elif lon < -180:
      lon = lon + 360
      self.flagE = 'E'
    else:
      self.lon = lon

    if lat < 0:
      lat = lat *- 1
      self.flagN = 'S'

    self.lonDeg = int(lon)
    self.latDeg = int(lat)
    self.lonMin = (lon - self.lonDeg) * 60
    self.latMin = (lat - self.latDeg) * 60

  def getMountPointString(self):

    mountPointString = 'GET %s HTTP/1.1\r\nUser-Agent: %s\r\nAuthorization: Basic %s\r\n' % (self.mountpoint, 'NTRIP JCMBsoftPythonClient/0.2', self.user) + '\r\n'

    if self.verbose:
      print(mountPointString)

    return mountPointString

  def getGGAString(self):

    now = datetime.datetime.utcnow()

    ggaString = 'GPGGA,%02d%02d%04.2f,%02d%011.8f,%1s,%03d%011.8f,%1s,1,05,0.19,+00400,M,%5.3f,M,,' % \
      (now.hour, now.minute, now.second, self.latDeg, self.latMin, self.flagN, self.lonDeg, self.lonMin, self.flagE, self.height)
    checksum = self.calcultateCheckSum(ggaString)

    if self.verbose:
      print('$%s*%s\r\n' % (ggaString, checksum))

    return '$%s*%s\r\n' % (ggaString, checksum)

  def calcultateCheckSum(self, stringToCheck):

    xsum_calc = 0

    for char in stringToCheck:
      xsum_calc = xsum_calc ^ ord(char)

    return '%02X' % xsum_calc

  def readData(self, hub):

    conn = socket.socket()
    conn.connect((self.server, self.port))
    conn.settimeout(10)
    conn.sendall(self.getMountPointString().encode())

    while not self.terminate:

      response = conn.recv(4096)

      if not response:
        break

      for line in response.split(b'\r\n'):
        if line.find(b'SOURCETABLE') >= 0:        raise Exception('Mount point does not exist')
        elif line.find(b'401 Unauthorized') >= 0: raise Exception('Unauthorized request')
        elif line.find(b'404 Not Found') >= 0:    raise Exception('Mount Point does not exist')
        elif line.find(b'ICY 200 OK') >= 0:       conn.sendall(self.getGGAString().encode())
        elif line.find(b'HTTP/1.0 200 OK') >= 0:  conn.sendall(self.getGGAString().encode())
        elif line.find(b'HTTP/1.1 200 OK') >= 0:  conn.sendall(self.getGGAString().encode())

      responseLength = len(response)
      
      progress = 0
      self.progress.emit(progress)

      while len(response) > 0:

        length = min(len(response), 32)
        chunk = response[:length]
        response = response[length:]

        progress += len(chunk) * 100 / responseLength
        self.progress.emit(progress)
        
        print(chunk)

        packet = {'id': proto.Message.COMPONENT_RAW_DATA, 'component': self.device.address, 'payload': chunk}
        hub.messenger.invokeAsync(packet = packet, callback = None)

    if self.verbose:
      print('Closing Connection\n')

    self.progress.emit(0)
    conn.close()
