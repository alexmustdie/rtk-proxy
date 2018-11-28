from PyQt5.QtWidgets import QLineEdit

from UI.OptionsDialog import OptionsDialog

class NtripOptionsDialog(OptionsDialog):

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
