from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QDialogButtonBox
from config import Config

class Options(QDialog):

  def __init__(self):
    
    super(Options, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    self.config = Config('config/NTRIP.json')
    fields = self.config.load()

    self.server = QLineEdit(fields['server'])
    grid.addWidget(QLabel('IP'), 1, 0)
    grid.addWidget(self.server, 1, 1)

    self.port = QLineEdit(fields['port'])
    grid.addWidget(QLabel('port'), 2, 0)
    grid.addWidget(self.port, 2, 1)

    self.mountpoint = QLineEdit(fields['mountpoint'])
    grid.addWidget(QLabel('mountpoint'), 3, 0)
    grid.addWidget(self.mountpoint, 3, 1)

    self.user = QLineEdit(fields['user'])
    grid.addWidget(QLabel('user'), 4, 0)
    grid.addWidget(self.user, 4, 1)

    self.password = QLineEdit(fields['password'])
    grid.addWidget(QLabel('password'), 5, 0)
    grid.addWidget(self.password, 5, 1)
    
    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    grid.addWidget(buttonBox, 6, 0, 1, 0)

    self.setLayout(grid)
    self.setWindowTitle('Опции NTRIP')
    self.setFixedSize(200, 0)

  def serialize(self):
    return {
      'server': self.server.text(),
      'port': self.port.text(),
      'mountpoint': self.mountpoint.text(),
      'user': self.user.text(),
      'password': self.password.text()
    }

  def accept(self):
    self.config.save(self.serialize())
    super(Options, self).accept()
