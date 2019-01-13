from PyQt5.QtWidgets import QComboBox

from UI.OptionsDialog import OptionsDialog
from logic.utils import getSerialPorts

class BaseStationOptionsDialog(OptionsDialog):

  configFilePath = 'config/base_station.json'

  def __init__(self):

    super().__init__(self.configFilePath, 'Опции базовой станции')

    fields = self.config.load()

    self.serial = QComboBox()
    self.serial.addItems(getSerialPorts())
    index = self.serial.findText(fields['serial'])
    if index >= 0: self.serial.setCurrentIndex(index)
    self.addRow('COM-порт', self.serial)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['9600', '19200', '38400', '57600', '115200', '230400', '460800'])
    index = self.baudrate.findText(str(fields['baudrate']))
    if index >= 0: self.baudrate.setCurrentIndex(index)
    self.addRow('Скорость порта', self.baudrate)

    self.addButtonBox()
    self.setFixedSize(250, 0)

  def serialize(self):

    serial = self.serial.currentText()
    baudrate = self.baudrate.currentText()

    if not serial:
      raise Exception('Не указан COM-порт')

    return {
      'serial': serial,
      'baudrate': int(baudrate)
    }
