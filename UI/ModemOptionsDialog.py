from PyQt5.QtWidgets import QLineEdit, QComboBox

from UI.OptionsDialog import OptionsDialog

class ModemOptionsDialog(OptionsDialog):

  configFilePath = 'config/modem.json'

  def __init__(self):

    super().__init__(self.configFilePath, 'Опции модема')

    fields = self.config.load()

    self.address = QLineEdit(fields['address'])
    self.addRow('Адрес', self.address)

    self.port = QLineEdit(str(fields['port']))
    self.addRow('Порт', self.port)

    self.modemAddress = QLineEdit(str(fields['modemAddress']))
    self.addRow('Адрес модема', self.modemAddress)

    self.modemPort = QLineEdit(str(fields['modemPort']))
    self.addRow('Порт модема', self.modemPort)

    self.device = QLineEdit(str(fields['device']))
    self.device.setPlaceholderText('Имя или адрес')
    self.addRow('Устройство', self.device)

    self.addButtonBox()
    self.setFixedSize(220, 0)

  def serialize(self):

    address = self.address.text()
    port = self.port.text()
    modemAddress = self.modemAddress.text()
    modemPort = self.modemPort.text()
    device = self.device.text()

    if not address:
      raise Exception('Не указан адрес')

    if not port:
      raise Exception('Не указан порт')

    if not modemAddress:
      raise Exception('Не указан адрес модема')

    if not modemPort:
      raise Exception('Не указан порт модема')

    if not device:
      raise Exception('Введите имя или номер устройства')

    return {
      'address': address,
      'port': int(port),
      'modemAddress': int(modemAddress),
      'modemPort': int(modemPort),
      'device': int(device) if device.isdigit() else device
    }
