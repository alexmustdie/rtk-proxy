from PyQt5.QtWidgets import QMessageBox, QDialog, QGridLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox

from config import Config
from utils import getSerialPorts

class AlertBox(QMessageBox):

  def __init__(self, message):
    super().__init__()
    self.setIcon(QMessageBox.Critical)
    self.setWindowTitle('Ошибка')
    self.setText(message)

class Options(QDialog):

  rowsCount = 0
  
  def __init__(self, configFilePath, title):

    super().__init__()

    self.config = Config(configFilePath)
    self.setWindowTitle(title)

    self.grid = QGridLayout()
    self.grid.setSpacing(10)
    self.setLayout(self.grid)

  def addRow(self, labelText, editObject):
    self.grid.addWidget(QLabel(labelText), self.rowsCount, 0)
    self.grid.addWidget(editObject, self.rowsCount, 1)
    self.rowsCount += 1

  def addButtonBox(self):
    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    self.grid.addWidget(buttonBox, self.rowsCount, 0, 1, 0)

  def accept(self):
    self.config.save(self.serialize())
    super().accept()

class AutopilotOptions(Options):

  def __init__(self):

    super().__init__('config/autopilot.json', 'Опции автопилота')

    fields = self.config.load()

    self.serial = QComboBox()
    self.serial.addItems(getSerialPorts())
    index = self.serial.findText(fields['serial'])
    if index >= 0: self.serial.setCurrentIndex(index)
    self.addRow('Устройство COM-порта', self.serial)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['57600', '115200', '230400', '460800', '500000', '921600', '1000000', '1500000', '2000000'])
    index = self.baudrate.findText(fields['baudrate'])
    if index >= 0: self.baudrate.setCurrentIndex(index)
    self.addRow('Скорость порта', self.baudrate)

    self.device = QLineEdit(fields['device'])
    self.addRow('Имя устройства в автопилоте', self.device)

    self.addButtonBox()
    self.setFixedSize(300, 0)

  def serialize(self):
    return {
      'serial': self.serial.currentText(),
      'baudrate': self.baudrate.currentText(),
      'device': self.device.text(),
    }

class BaseStationOptions(Options):

  def __init__(self):
    
    super().__init__('config/baseStation.json', 'Опции базовой станции')

    fields = self.config.load()

    self.serial = QComboBox()
    self.serial.addItems(getSerialPorts())
    index = self.serial.findText(fields['serial'])
    if index >= 0: self.serial.setCurrentIndex(index)
    self.addRow('Устройство COM-порта', self.serial)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['9600', '19200', '38400', '57600', '115200', '230400', '460800'])
    index = self.baudrate.findText(fields['baudrate'])
    if index >= 0: self.baudrate.setCurrentIndex(index)
    self.addRow('Скорость порта', self.baudrate)

    self.addButtonBox()
    self.setFixedSize(270, 0)

  def serialize(self):
    return {
      'serial': self.serial.currentText(),
      'baudrate': self.baudrate.currentText()
    }

class NtripOptions(Options):

  def __init__(self):

    super().__init__('config/NTRIP.json', 'Опции NTRIP')

    fields = self.config.load()

    self.server = QLineEdit(fields['server'])
    self.addRow('IP', self.server)

    self.port = QLineEdit(fields['port'])
    self.addRow('port', self.port)

    self.mountpoint = QLineEdit(fields['mountpoint'])
    self.addRow('mountpoint', self.mountpoint)

    self.user = QLineEdit(fields['user'])
    self.addRow('user', self.user)

    self.password = QLineEdit(fields['password'])
    self.password.setEchoMode(QLineEdit.Password)
    self.addRow('password', self.password)

    self.addButtonBox()
    self.setFixedSize(200, 0)

  def serialize(self):
    return {
      'server': self.server.text(),
      'port': self.port.text(),
      'mountpoint': self.mountpoint.text(),
      'user': self.user.text(),
      'password': self.password.text()
    }
