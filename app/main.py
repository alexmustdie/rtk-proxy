#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from dialogs.autopilot import *
from dialogs.baseStation import *
from dialogs.NTRIP import *

class MainWindow(QWidget):

  # TODO: сделать индикацию

  def __init__(self):
    
    super(MainWindow, self).__init__()

    grid = QGridLayout()
    grid.setSpacing(10)

    # 1 row

    streamLabel = QLabel('Поток')
    grid.addWidget(streamLabel, 0, 0)
    streamLabel.setAlignment(Qt.AlignCenter)

    typeLabel = QLabel('Тип')
    grid.addWidget(typeLabel, 0, 1)
    typeLabel.setAlignment(Qt.AlignCenter)

    optionsLabel = QLabel('Опции')
    grid.addWidget(optionsLabel, 0, 2)
    optionsLabel.setAlignment(Qt.AlignCenter)

    # 2 row

    grid.addWidget(QLabel('Входной'), 1, 0)
    
    self.inputStreamType = QComboBox()
    self.inputStreamType.addItems(['Базовая станция', 'NTRIP'])
    grid.addWidget(self.inputStreamType, 1, 1)

    inputSreamOptionsButton = QPushButton('...')
    inputSreamOptionsButton.clicked.connect(self.showInputStreamOptions)
    grid.addWidget(inputSreamOptionsButton, 1, 2)

    # 3 row

    grid.addWidget(QLabel('Выходной'), 2, 0)

    grid.addWidget(QLabel('Aвтопилот'), 2, 1)

    autopilotOptionsButton = QPushButton('...')
    autopilotOptionsButton.clicked.connect(self.showAutopilotOptions)
    grid.addWidget(autopilotOptionsButton, 2, 2)

    # 4 row

    startButton = QPushButton('Запустить')
    grid.addWidget(startButton, 3, 0)

    stopButton = QPushButton('Остановить')
    grid.addWidget(stopButton, 3, 1)

    exitButton = QPushButton('Выйти')
    exitButton.clicked.connect(self.exit)
    grid.addWidget(exitButton, 3, 2)
    
    self.setLayout(grid)
    self.setGeometry(300, 300, 0, 0)
    self.setFixedSize(0, 0)

  def showInputStreamOptions(self):
    index = self.inputStreamType.currentIndex()
    if index == 0:
      dialog = BaseStationOptionsDialog()
      if (dialog.exec_() == QDialog.Accepted):
        print(dialog.serial.text())
        print(dialog.baudrate.currentIndex())
    else:
      if index == 1:
        dialog = NtripOptionsDialog()
        if (dialog.exec_() == QDialog.Accepted):
          print(dialog.ip.text())
          print(dialog.port.text())
          print(dialog.mountpoint.text())
          print(dialog.user.text())
          print(dialog.password.text())

  def showAutopilotOptions(self):
    dialog = AutopilotOptionsDialog()
    if (dialog.exec_() == QDialog.Accepted):
      print(dialog.serial.text())
      print(dialog.baudrate.currentIndex())
      print(dialog.hub.text())

  def exit(self):
    self.close()

if __name__ == '__main__':

  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
