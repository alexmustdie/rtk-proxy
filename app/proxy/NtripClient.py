import socket
import datetime
import base64
import time

from proxy import proto

version = 0.2
useragent = 'NTRIP JCMBsoftPythonClient/%.1f' % version

class NtripClient(object):

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

    self.buffer = buffer
    self.user = base64.b64encode((user + ':' + password).encode()).decode()
    self.port = int(port)
    self.server = server
    self.mountpoint = mountpoint
    self.setPosition(lat, lon)
    self.height = height
    self.verbose = verbose
    self.socket = None

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

    mountPointString = 'GET %s HTTP/1.1\r\nUser-Agent: %s\r\nAuthorization: Basic %s\r\n' % (self.mountpoint, useragent, self.user) + '\r\n'

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

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect_ex((self.server, self.port))
    self.socket.settimeout(10)
    self.socket.sendall(self.getMountPointString().encode())

    while True:

      response = self.socket.recv(4096)

      if not response:
        break

      while len(response) > 0:

        length = min(len(response), 32)
        chunk = response[:length]
        response = response[length:]

        print(chunk)

        packet = {'id': proto.Message.COMPONENT_RAW_DATA, 'component': hub['Ublox'].address, 'payload': chunk}
        hub.messenger.invokeAsync(packet = packet, callback = None)

    if self.verbose:
      print('Closing Connection\n')

    self.socket.close()
    self.socket = None
