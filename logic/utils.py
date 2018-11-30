import serial.tools.list_ports

def getSerialPorts():

  comPorts = serial.tools.list_ports.comports()

  result = []

  for comPort in comPorts:
    result.append(comPort.device)

  return result
