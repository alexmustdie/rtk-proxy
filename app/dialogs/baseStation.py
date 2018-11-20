from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox

from config import Config
from utils import getSerialPorts

class Options(QDialog):

  def __init__(self):
    
    super(Options, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    self.config = Config('config/baseStation.json')
    fields = self.config.load()

    self.serial = QComboBox()
    self.serial.addItems(getSerialPorts())
    index = self.serial.findText(fields['serial'])
    if index >= 0:
      self.serial.setCurrentIndex(index)
    grid.addWidget(QLabel('Устройство COM-порта'), 1, 0)
    grid.addWidget(self.serial, 1, 1)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['9600', '19200', '38400', '57600', '115200', '230400', '460800'])
    index = self.baudrate.findText(fields['baudrate'])
    if index >= 0:
      self.baudrate.setCurrentIndex(index)
    grid.addWidget(QLabel('Скорость порта'), 2, 0)
    grid.addWidget(self.baudrate, 2, 1)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    grid.addWidget(buttonBox, 4, 0, 1, 0)

    self.setLayout(grid)
    self.setWindowTitle('Опции базовой станции')
    self.setFixedSize(270, 0)

  def serialize(self):
    return {
      'serial': self.serial.currentText(),
      'baudrate': self.baudrate.currentText()
    }

  def accept(self):
    self.config.save(self.serialize())
    super(Options, self).accept()
