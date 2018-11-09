#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class autopilotOptionsDialog(QDialog):

  def __init__(self):
    
    super(autopilotOptionsDialog, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    self.serial = QLineEdit()
    grid.addWidget(QLabel('Устройство COM-порта'), 1, 0)
    grid.addWidget(self.serial, 1, 1)

    self.baudrate = QComboBox()
    self.baudrate.addItems(['57600', '115200', '230400', '460800', '500000', '921600', '1000000', '1500000', '2000000'])
    grid.addWidget(QLabel('Скорость порта'), 2, 0)
    grid.addWidget(self.baudrate, 2, 1)

    self.hub = QLineEdit('Ublox')
    grid.addWidget(QLabel('Имя устройства в автопилоте'), 3, 0)
    grid.addWidget(self.hub, 3, 1)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    grid.addWidget(buttonBox, 4, 0, 1, 0)

    self.setLayout(grid)
    self.setWindowTitle("Опции автопилота")
    self.setMinimumWidth(350)

class baseStationOptionsDialog(QDialog):

  def __init__(self):
    
    super(baseStationOptionsDialog, self).__init__()

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

class ntripOptionsDialog(QDialog):

  def __init__(self):
    
    super(ntripOptionsDialog, self).__init__()

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

class MainWindow(QWidget):

  # TODO: сделать разделение полей и индикацию

  def __init__(self):
    
    super(MainWindow, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(QLabel('Aвтопилот'), 0, 0)
  
    autopilotOptionsButton = QPushButton('Опции')
    autopilotOptionsButton.clicked.connect(self.showAutopilotOptions)
    grid.addWidget(autopilotOptionsButton, 0, 1)

    self.inputStreamType = QComboBox()
    self.inputStreamType.addItems(['Базовая станция', 'NTRIP'])
    grid.addWidget(self.inputStreamType, 1, 0)

    inputSreamOptionsButton = QPushButton('Опции')
    inputSreamOptionsButton.clicked.connect(self.showInputStreamOptions)
    grid.addWidget(inputSreamOptionsButton, 1, 1)

    startButton = QPushButton('Запустить')
    stopButton = QPushButton('Остановить')

    grid.addWidget(startButton, 2, 0)
    grid.addWidget(stopButton, 2, 1)
    
    self.setLayout(grid)

  def showAutopilotOptions(self):
    autopilotOptionsDialog().exec_()

  def showInputStreamOptions(self):
    if self.inputStreamType.currentIndex() == 0:
      baseStationOptionsDialog().exec_()
    else:
      if self.inputStreamType.currentIndex() == 1:
        ntripOptionsDialog().exec_()


if __name__ == '__main__':

  app = QApplication(sys.argv)
  window = MainWindow()
  window.setGeometry(300, 300, 350, 0)
  window.setWindowTitle('RTK proxy')
  window.show()
  sys.exit(app.exec_())
