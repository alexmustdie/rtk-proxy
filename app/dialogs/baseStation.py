from PyQt5.QtWidgets import *

class BaseStationOptionsDialog(QDialog):

  def __init__(self):
    
    super(BaseStationOptionsDialog, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    self.serial = QLineEdit()
    grid.addWidget(QLabel('Устройство COM-порта'), 1, 0)
    grid.addWidget(self.serial, 1, 1)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['9600', '19200', '38400', '57600', '115200', '230400', '460800'])
    grid.addWidget(QLabel('Скорость порта'), 2, 0)
    grid.addWidget(self.baudrate, 2, 1)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    grid.addWidget(buttonBox, 4, 0, 1, 0)

    self.setLayout(grid)
    self.setWindowTitle("Опции базовой станции")
    self.setMinimumWidth(300)
