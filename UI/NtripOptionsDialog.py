from PyQt5.QtWidgets import QLineEdit

from UI.OptionsDialog import OptionsDialog

class NtripOptionsDialog(OptionsDialog):

  configFilePath = 'config/NTRIP.json'

  def __init__(self):

    super().__init__(self.configFilePath, 'Опции NTRIP')

    fields = self.config.load()

    self.server = QLineEdit(fields['server'])
    self.addRow('IP сервера', self.server)

    self.port = QLineEdit(str(fields['port']))
    self.addRow('Порт', self.port)

    self.mountpoint = QLineEdit(fields['mountpoint'])
    self.addRow('Точка монтирования', self.mountpoint)

    self.user = QLineEdit(fields['user'])
    self.addRow('Пользователь', self.user)

    self.password = QLineEdit(fields['password'])
    self.password.setEchoMode(QLineEdit.Password)
    self.addRow('Пароль', self.password)

    self.addButtonBox()
    self.setFixedSize(250, 0)

  def serialize(self):

    server = self.server.text()
    port = self.port.text()
    mountpoint = self.mountpoint.text()
    user = self.user.text()
    password = self.password.text()

    if not server:
      raise Exception('Не указан IP сервера')

    if not port:
      raise Exception('Не указан порт')

    if not mountpoint:
      raise Exception('Не указана точка монтирования')

    if not user:
      raise Exception('Не указан пользователь')

    if not password:
      raise Exception('Не указан пароль')

    return {
      'server': server,
      'port': int(port),
      'mountpoint': mountpoint,
      'user': user,
      'password': password
    }
