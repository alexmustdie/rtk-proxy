import serial.tools.list_ports   # import serial module
comPorts = list(serial.tools.list_ports.comports())    # get list of all devices connected through serial port

print('List of devices connected on com ports : ', comPorts)

numPortsUsed = len(comPorts)   # get number of com ports used   # get number of com ports used in system

print('Number of com ports used in system : ', numPortsUsed)
