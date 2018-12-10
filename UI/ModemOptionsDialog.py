from PyQt5.QtWidgets import QLineEdit, QComboBox

from UI.OptionsDialog import OptionsDialog

class ModemOptionsDialog(OptionsDialog):

  def __init__(self):

    super().__init__('config/modem.json', 'Опции модема')

    fields = self.config.load()

    self.address = QLineEdit(fields['address'])
    self.addRow('Адрес', self.address)

    self.port = QLineEdit(fields['port'])
    self.addRow('Порт', self.port)

    self.modemAddress = QLineEdit(fields['modemAddress'])
    self.addRow('Адрес модема', self.modemAddress)

    self.modemPort = QLineEdit(fields['modemPort'])
    self.addRow('Порт модема', self.modemPort)

    self.device = QLineEdit(fields['device'])
    self.addRow('Имя устройства', self.device)

    self.addButtonBox()
    self.setFixedSize(200, 0)

  def serialize(self):
    return {
      'address': self.address.text(),
      'port': self.port.text(),
      'modemAddress': self.modemAddress.text(),
      'modemPort': self.modemPort.text(),
      'device': self.device.text()
    }
