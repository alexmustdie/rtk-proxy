#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Example(QWidget):

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):

    grid = QGridLayout()
    grid.setSpacing(10)

    #autopilot part

    autopilotLabel = QLabel('Aвтопилот')
    autopilotLabel.setAlignment(Qt.AlignCenter)
    grid.addWidget(autopilotLabel, 0, 0, 1, 0)

    autopilotSerialEdit = QLineEdit()
    grid.addWidget(QLabel('Устройство COM-порта'), 1, 0)
    grid.addWidget(autopilotSerialEdit, 1, 1)

    autopilotBaudrateComboBox = QComboBox()
    autopilotBaudrateComboBox.addItems(['57600', '115200', '230400', '460800', '500000', '921600', '1000000', '1500000', '2000000'])
    grid.addWidget(QLabel('Скорость порта'), 2, 0)
    grid.addWidget(autopilotBaudrateComboBox, 2, 1)

    hubEdit = QLineEdit('Ublox')
    grid.addWidget(QLabel('Имя устройства в автопилоте'), 3, 0)
    grid.addWidget(hubEdit, 3, 1)

    #base station part

    '''baseStationLabel = QLabel('Базовая станция')
    baseStationLabel.setAlignment(Qt.AlignCenter)
    grid.addWidget(baseStationLabel, 4, 0, 1, 0)

    baseStationSerialEdit = QLineEdit()
    grid.addWidget(QLabel('Устройство COM-порта'), 5, 0)
    grid.addWidget(baseStationSerialEdit, 5, 1)

    baseStationComboBox = QComboBox()
    baseStationComboBox.addItems(['9600', '19200', '38400', '57600', '115200', '230400', '460800'])
    grid.addWidget(QLabel('Скорость порта'), 6, 0)
    grid.addWidget(baseStationComboBox, 6, 1)'''

    #ntrip part
    
    ntripLabel = QLabel('Ntrip')
    ntripLabel.setAlignment(Qt.AlignCenter)
    grid.addWidget(ntripLabel, 4, 0, 1, 0)

    ipEdit = QLineEdit()
    grid.addWidget(QLabel('IP'), 5, 0)
    grid.addWidget(ipEdit, 5, 1)

    portEdit = QLineEdit()
    grid.addWidget(QLabel('port'), 6, 0)
    grid.addWidget(portEdit, 6, 1)

    mountpointEdit = QLineEdit()
    grid.addWidget(QLabel('mountpoint'), 7, 0)
    grid.addWidget(mountpointEdit, 7, 1)

    userEdit = QLineEdit()
    grid.addWidget(QLabel('user'), 8, 0)
    grid.addWidget(userEdit, 8, 1)

    passwordEdit = QLineEdit()
    grid.addWidget(QLabel('password'), 9, 0)
    grid.addWidget(passwordEdit, 9, 1)

    runButton = QPushButton("Запустить")
    grid.addWidget(runButton, 10, 0, 1, 0)

    self.setLayout(grid)
    self.setGeometry(300, 300, 350, 0)
    self.setWindowTitle('First Task')
    self.show()

if __name__ == '__main__':

  app = QApplication(sys.argv)
  ex = Example()
  sys.exit(app.exec_())
