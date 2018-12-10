import serial.tools.list_ports
import re

def getSerialPorts():

  ports = serial.tools.list_ports.comports()
  result = []

  for port in ports:
    if not re.match(r'^\/dev\/ttyS[0-3]$', port.device):
      result.append(port.device)

  return result
