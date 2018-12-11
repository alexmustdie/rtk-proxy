from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QComboBox, QRadioButton

from UI.OptionsDialog import OptionsDialog
from logic.utils import getSerialPorts

class AutopilotOptionsDialog(OptionsDialog):

  def __init__(self):

    super().__init__('config/autopilot.json', 'Опции автопилота')

    fields = self.config.load()

    self.serial = QComboBox()
    self.serial.addItems(getSerialPorts())
    index = self.serial.findText(fields['serial'])
    if index >= 0: self.serial.setCurrentIndex(index)
    self.addRow('COM-порт', self.serial)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['57600', '115200', '230400', '460800', '500000', '921600', '1000000', '1500000', '2000000'])
    index = self.baudrate.findText(str(fields['baudrate']))
    if index >= 0: self.baudrate.setCurrentIndex(index)
    self.addRow('Скорость порта', self.baudrate)

    self.device = QLineEdit(str(fields['device']))
    self.device.setPlaceholderText('Имя или адрес')
    self.addRow('Устройство', self.device)

    self.addButtonBox()
    self.setFixedSize(250, 0)

  def serialize(self):

    serial = self.serial.currentText()
    baudrate = self.baudrate.currentText()
    device = self.device.text()

    if not serial:
      raise Exception('Не указан COM-порт')

    if not device:
      raise Exception('Введите имя или номер устройства')

    return {
      'serial': serial,
      'baudrate': int(baudrate),
      'device': int(device) if device.isdigit() else device
    }
