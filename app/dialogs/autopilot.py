from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox

from config import Config
from utils import getSerialPorts

class Options(QDialog):

  def __init__(self):

    super(Options, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    self.config = Config('config/autopilot.json')
    fields = self.config.load()

    self.serial = QComboBox()
    self.serial.addItems(getSerialPorts())
    index = self.serial.findText(fields['serial'])
    if index >= 0:
      self.serial.setCurrentIndex(index)
    grid.addWidget(QLabel('Устройство COM-порта'), 1, 0)
    grid.addWidget(self.serial, 1, 1)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['57600', '115200', '230400', '460800', '500000', '921600', '1000000', '1500000', '2000000'])
    index = self.baudrate.findText(fields['baudrate'])
    if index >= 0:
      self.baudrate.setCurrentIndex(index)
    grid.addWidget(QLabel('Скорость порта'), 2, 0)
    grid.addWidget(self.baudrate, 2, 1)

    self.hub = QLineEdit(fields['hub'])
    grid.addWidget(QLabel('Имя устройства в автопилоте'), 3, 0)
    grid.addWidget(self.hub, 3, 1)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    grid.addWidget(buttonBox, 4, 0, 1, 0)

    self.setLayout(grid)
    self.setWindowTitle('Опции автопилота')
    self.setFixedSize(300, 0)

  def serialize(self):
    return {
      'serial': self.serial.currentText(),
      'baudrate': self.baudrate.currentText(),
      'hub': self.hub.text(),
    }

  def accept(self):
    self.config.save(self.serialize())
    super(Options, self).accept()
