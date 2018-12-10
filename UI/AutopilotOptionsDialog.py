from PyQt5.QtWidgets import QLineEdit, QComboBox

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
    self.addRow('Устройство COM-порта', self.serial)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['57600', '115200', '230400', '460800', '500000', '921600', '1000000', '1500000', '2000000'])
    index = self.baudrate.findText(fields['baudrate'])
    if index >= 0: self.baudrate.setCurrentIndex(index)
    self.addRow('Скорость порта', self.baudrate)

    self.device = QLineEdit(fields['device'])
    self.addRow('Имя устройства', self.device)

    self.addButtonBox()
    self.setFixedSize(300, 0)

  def serialize(self):
    return {
      'serial': self.serial.currentText(),
      'baudrate': self.baudrate.currentText(),
      'device': self.device.text(),
    }
