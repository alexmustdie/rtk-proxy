#!/usr/bin/env python3

import socket
import sys
import datetime
import base64
import signal
import time
from optparse import OptionParser

from proxy import proto

version = 0.2
useragent = 'NTRIP JCMBsoftPythonClient/%.1f' % version

factor = 2
maxReconnect = 1
maxReconnectTime = 1200
sleepTime = 1
maxConnectTime = 0

termRequest = False

class NtripClient(object):

  def __init__(self,
     buffer = 50,
     user = '',
     password = '',
     out = sys.stdout,
     port = 2101,
     caster = '',
     mountpoint = '',
     lat = 46,
     lon = 122,
     height = 1212,
     verbose = False):

    self.buffer = buffer
    self.user = base64.b64encode((user+":"+password).encode()).decode()
    self.out = out
    self.port = int(port)
    self.caster = caster
    self.mountpoint = mountpoint
    self.setPosition(lat, lon)
    self.height = height
    self.verbose = verbose
    self.maxConnectTime = maxConnectTime
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

  def terminateHandler(signum, frame):
    global termRequest
    print('Termination requested')
    termRequest = True

  def readData(self, hub):

    global termRequest
    signal.signal(signal.SIGINT, self.terminateHandler)

    reconnectTry = 1
    sleepTime = 1
    reconnectTime = 0

    if maxConnectTime > 0:
      EndConnect = datetime.timedelta(seconds = maxConnectTime)
    try:
      while reconnectTry <= maxReconnect:

        if self.verbose:
          sys.stderr.write('Connection {0} of {1}\n'.format(reconnectTry, maxReconnect))

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        error_indicator = self.socket.connect_ex((self.caster, self.port))

        if error_indicator == 0:

          sleepTime = 1
          connectTime = datetime.datetime.now()

          self.socket.settimeout(10)
          self.socket.sendall(self.getMountPointString().encode())

          while not termRequest:

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

            for line in response.split(b'\r\n'):
              if line.find(b'SOURCETABLE') >= 0:
                sys.stderr.write('Mount point does not exist')
                sys.exit(1)
              elif line.find(b'401 Unauthorized') >= 0:
                sys.stderr.write('Unauthorized request\n')
                sys.exit(1)
              elif line.find(b'404 Not Found') >= 0:
                sys.stderr.write('Mount Point does not exist\n')
                sys.exit(2)
              elif line.find(b'ICY 200 OK') >= 0:
                self.socket.sendall(self.getGGAString().encode())
              elif line.find(b'HTTP/1.0 200 OK') >= 0:
                self.socket.sendall(self.getGGAString().encode())
              elif line.find(b'HTTP/1.1 200 OK') >= 0:
                self.socket.sendall(self.getGGAString().encode())

          data = 'Initial data'

          while data:
            try:
              data = self.socket.recv(self.buffer)
              if maxConnectTime:
                if datetime.datetime.now() > connectTime + EndConnect:
                  if self.verbose:
                    sys.stderr.write('Connection Timed exceeded\n')
                  sys.exit(0)

            except socket.timeout:
              if self.verbose:
                sys.stderr.write('Connection TimedOut\n')
              data = False

            except socket.error:
              if self.verbose:
                sys.stderr.write('Connection Error\n')
              data = False

          if self.verbose:
            sys.stderr.write('Closing Connection\n')

          self.socket.close()
          self.socket = None

          if reconnectTry < maxReconnect:

            sys.stderr.write('%s No Connection to NtripCaster.  Trying again in %i seconds\n' % (datetime.datetime.now(), sleepTime))
            time.sleep(sleepTime)
            sleepTime *=  factor

            if sleepTime > maxReconnectTime:
              sleepTime = maxReconnectTime

          reconnectTry += 1
        else:
          self.socket = None

          if self.verbose:
            print('Error indicator: ', error_indicator)

          if reconnectTry < maxReconnect:

            sys.stderr.write('%s No Connection to NtripCaster.  Trying again in %i seconds\n' % (datetime.datetime.now(), sleepTime))
            time.sleep(sleepTime)
            sleepTime *= factor

            if sleepTime > maxReconnectTime:
              sleepTime = maxReconnectTime

          reconnectTry +=  1

    except KeyboardInterrupt:
      if self.socket:
        self.socket.close()
      sys.exit()

# if __name__ ==  '__main__':

#   ntripArgs = {}

#   ntripArgs['lat'] = 50.09
#   ntripArgs['lon'] = 8.66
#   ntripArgs['height'] = 1200
#   ntripArgs['user'] = 'user1:123456'
#   ntripArgs['caster'] = '10.10.0.51'
#   ntripArgs['port'] = 2101
#   ntripArgs['mountpoint'] = 'sss'
#   ntripArgs['verbose'] = True

#   if ntripArgs['mountpoint'][0:1] != '/':
#     ntripArgs['mountpoint'] = '/' + ntripArgs['mountpoint']

#   if ntripArgs['verbose']:
#     print('Server: ' + ntripArgs['caster'])
#     print('Port: ' + str(ntripArgs['port']))
#     print('User: ' + ntripArgs['user'])
#     print('mountpoint: ' + ntripArgs['mountpoint'])
#     print('Reconnects: ' + str(maxReconnect))
#     print('Max Connect Time: ' + str(maxConnectTime))
#     print()

#   proto.verboseEnabled = True
#   stream = proto.SerialStream('/dev/ttyUSB0', 57600)
#   messenger = proto.Messenger(stream, 'cache')
#   messenger.connect()
#   time.sleep(2)

#   if messenger.hub['Ublox'] is not None:
#     n = NtripClient(**ntripArgs)
#     n.readData(messenger.hub)
#   else:
#     print('Ublox not found')
