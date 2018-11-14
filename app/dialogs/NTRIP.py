from PyQt5.QtWidgets import *

class NtripOptionsDialog(QDialog):

  def __init__(self):
    
    super(NtripOptionsDialog, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    self.ip = QLineEdit()
    grid.addWidget(QLabel('IP'), 1, 0)
    grid.addWidget(self.ip, 1, 1)

    self.port = QLineEdit()
    grid.addWidget(QLabel('port'), 2, 0)
    grid.addWidget(self.port, 2, 1)

    self.mountpoint = QLineEdit()
    grid.addWidget(QLabel('mountpoint'), 3, 0)
    grid.addWidget(self.mountpoint, 3, 1)

    self.user = QLineEdit()
    grid.addWidget(QLabel('user'), 4, 0)
    grid.addWidget(self.user, 4, 1)

    self.password = QLineEdit()
    grid.addWidget(QLabel('password'), 5, 0)
    grid.addWidget(self.password, 5, 1)
    
    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    grid.addWidget(buttonBox, 6, 0, 1, 0)

    self.setLayout(grid)
    self.setWindowTitle("Опции NTRIP")
    self.setMinimumWidth(300)
    self.setFixedSize(0, 0)
