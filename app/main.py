#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from dialogs import autopilot, baseStation, NTRIP

from proxy import proto
from proxy.NtripClient import NtripClient

class MainWindow(QWidget):

  # TODO: сделать индикацию и кнопку остановки

  def __init__(self):
    
    super(MainWindow, self).__init__()

    self.autopilotOptions = autopilot.Options().serialize()
    self.ntripOptions = NTRIP.Options().serialize()

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

    self.startButton = QPushButton('Запустить')
    self.startButton.clicked.connect(self.start)
    grid.addWidget(self.startButton, 3, 0)

    stopButton = QPushButton('Остановить')
    stopButton.clicked.connect(self.stop)
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
      dialog = baseStation.Options()
      if (dialog.exec_() == QDialog.Accepted):
        print(dialog.serial.text())
        print(dialog.baudrate.currentText())
    else:
      if index == 1:
        dialog = NTRIP.Options()
        if (dialog.exec_() == QDialog.Accepted):
          self.ntripOptions = dialog.serialize()

  def showAutopilotOptions(self):
    dialog = autopilot.Options()
    if (dialog.exec_() == QDialog.Accepted):
      self.autopilotOptions = dialog.serialize()

  def start(self):

    self.startButton.setEnabled(False)

    if self.ntripOptions['mountpoint'][0:1] != '/':
      self.ntripOptions['mountpoint'] = '/' + self.ntripOptions['mountpoint']

    self.ntripOptions['lat'] = 50.09
    self.ntripOptions['lon'] = 8.66
    self.ntripOptions['height'] = 1200
    self.ntripOptions['verbose'] = True

    if self.ntripOptions['verbose']:
      print('server: ' + self.ntripOptions['server'])
      print('port: ' + str(self.ntripOptions['port']))
      print('user: ' + self.ntripOptions['user'])
      print('mountpoint: ' + self.ntripOptions['mountpoint'])
      print()
      print('serial: ' + self.autopilotOptions['serial'])
      print('baudrate: ' + self.autopilotOptions['baudrate'])
      print('hub: ' + self.autopilotOptions['hub'])
      print()

    stream = proto.SerialStream(self.autopilotOptions['serial'], self.autopilotOptions['baudrate'])

    messenger = proto.Messenger(stream, 'cache')
    messenger.connect()

    proto.verboseEnabled = False

    if messenger.hub[self.autopilotOptions['hub']] is not None:
      ntripClient = NtripClient(**self.ntripOptions)
      ntripClient.readData(messenger.hub)
    else:
      print('Ublox not found')

  def stop(self):
    self.startButton.setEnabled(True)
    print('stop clicked')

  def exit(self):
    self.close()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
