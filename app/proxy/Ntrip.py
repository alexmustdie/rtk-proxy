import sys
import socket
import datetime
import base64

from proxy import proto, Input

class Ntrip:

  class Thread(Input.Thread):

    def __init__(self, ntripOptions, autopilotOptions):

      super().__init__()

      if ntripOptions['mountpoint'][0:1] != '/':
        ntripOptions['mountpoint'] = '/' + ntripOptions['mountpoint']

      self.inputClient = Ntrip.Client(**ntripOptions)
      self.connectOutputClient(autopilotOptions)

  class Client(Input.Client):

    def __init__(self, user, password, port, server, mountpoint):

      super().__init__()

      self.user = base64.b64encode((user + ':' + password).encode()).decode()
      self.mountpoint = mountpoint
      self.setPosition(46, 122)
      self.height = 1212

      self.conn = socket.socket()
      self.conn.connect((server, int(port)))
      self.conn.settimeout(10)
      self.conn.sendall(self.getMountPointString().encode())

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
      return mountPointString

    def getGGAString(self):

      now = datetime.datetime.utcnow()

      ggaString = 'GPGGA,%02d%02d%04.2f,%02d%011.8f,%1s,%03d%011.8f,%1s,1,05,0.19,+00400,M,%5.3f,M,,' % \
        (now.hour, now.minute, now.second, self.latDeg, self.latMin, self.flagN, self.lonDeg, self.lonMin, self.flagE, self.height)
      checksum = self.calcultateCheckSum(ggaString)

      return '$%s*%s\r\n' % (ggaString, checksum)

    def calcultateCheckSum(self, stringToCheck):

      xsum_calc = 0

      for char in stringToCheck:
        xsum_calc = xsum_calc ^ ord(char)

      return '%02X' % xsum_calc

    def readData(self, hub):

      bytesCount = 0
      self.bytesCount.emit(bytesCount)

      while not self.terminate:

        response = self.conn.recv(256)

        if not response:
          break

        for line in response.split(b'\r\n'):
          if line.find(b'SOURCETABLE') >= 0:        raise Exception('Mount point does not exist')
          elif line.find(b'401 Unauthorized') >= 0: raise Exception('Unauthorized request')
          elif line.find(b'404 Not Found') >= 0:    raise Exception('Mount Point does not exist')
          elif line.find(b'ICY 200 OK') >= 0:       self.conn.sendall(self.getGGAString().encode())
          elif line.find(b'HTTP/1.0 200 OK') >= 0:  self.conn.sendall(self.getGGAString().encode())
          elif line.find(b'HTTP/1.1 200 OK') >= 0:  self.conn.sendall(self.getGGAString().encode())

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
