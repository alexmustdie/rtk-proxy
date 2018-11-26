#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from dialogs import alert, autopilot, baseStation, NTRIP
from proxy.NtripClient import NtripClientThread

class MainWindow(QWidget):

  inputStreamType = 0

  baseStationThread = None
  ntripClientThread = None

  def __init__(self):
    
    super(MainWindow, self).__init__()

    self.baseStationOptions = baseStation.Options().serialize()
    self.ntripOptions = NTRIP.Options().serialize()
    self.autopilotOptions = autopilot.Options().serialize()

    grid = QGridLayout()
    grid.setSpacing(10)

    # 1 row

    streamLabel = QLabel('Поток')
    grid.addWidget(streamLabel, 0, 0)

    typeLabel = QLabel('Тип')
    grid.addWidget(typeLabel, 0, 1)

    optionsLabel = QLabel('Опции')
    grid.addWidget(optionsLabel, 0, 2)

    for widget in (streamLabel, typeLabel, optionsLabel):
      widget.setStyleSheet("padding:5;background-color:lightgray;");
      widget.setAlignment(Qt.AlignCenter)

    # 2 row

    grid.addWidget(QLabel('Входной'), 1, 0)
    
    inputStreamTypeComboBox = QComboBox()
    inputStreamTypeComboBox.addItems(['Базовая станция', 'NTRIP'])
    inputStreamTypeComboBox.currentIndexChanged.connect(self.onInputStreamTypeChanged)
    grid.addWidget(inputStreamTypeComboBox, 1, 1)

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

    self.deviceStatusLabel = QLabel('Статус устройства')
    self.deviceStatusLabel.setFixedSize(330, 45)
    self.deviceStatusLabel.setStyleSheet("padding:5;background-color:lightgray;");
    self.deviceStatusLabel.setWordWrap(True)
    grid.addWidget(self.deviceStatusLabel, 3, 0, 1, 3)

    # 5 row

    self.progressBar = QProgressBar(self)
    self.progressBar.setFixedSize(330, 10)
    self.progressBar.setTextVisible(False)
    grid.addWidget(self.progressBar, 4, 0, 1, 3)

    # 6 row

    self.startButton = QPushButton('Запустить')
    self.startButton.clicked.connect(self.start)
    grid.addWidget(self.startButton, 5, 0)

    self.stopButton = QPushButton('Остановить')
    self.stopButton.setDisabled(True)
    self.stopButton.clicked.connect(self.stop)
    grid.addWidget(self.stopButton, 5, 1)

    exitButton = QPushButton('Выйти')
    exitButton.clicked.connect(self.exit)
    grid.addWidget(exitButton, 5, 2)

    # rows end
    
    self.setLayout(grid)
    self.setFixedSize(350, 0)
    self.setWindowTitle('RTK proxy')

  def onInputStreamTypeChanged(self, index):
    self.inputStreamType = index

  def showInputStreamOptions(self):
    if self.inputStreamType == 0:
      dialog = baseStation.Options()
      if (dialog.exec_() == QDialog.Accepted):
        print(dialog.serial.currentText())
        print(dialog.baudrate.currentText())
    else:
      dialog = NTRIP.Options()
      if (dialog.exec_() == QDialog.Accepted):
        self.ntripOptions = dialog.serialize()

  def showAutopilotOptions(self):
    dialog = autopilot.Options()
    if (dialog.exec_() == QDialog.Accepted):
      self.autopilotOptions = dialog.serialize()

  def showAlertBox(self, message):
    alert.Box(message).exec_()

  def updateDeviceStatus(self, status):
    self.deviceStatusLabel.setText(status)

  def setProgressBarValue(self, progress):
    self.progressBar.setValue(progress)

  def handleThreadException(self, message):
    self.showAlertBox(message)
    self.stop()

  def start(self):

    self.startButton.setEnabled(False)
    self.stopButton.setEnabled(True)

    try:

      if self.inputStreamType == 0:
        pass
      else:
        self.ntripClientThread = NtripClientThread(self.ntripOptions, self.autopilotOptions)
        self.ntripClientThread.start()
        self.ntripClientThread.deviceStatus.connect(self.updateDeviceStatus)
        self.ntripClientThread.progress.connect(self.setProgressBarValue)
        self.ntripClientThread.failed.connect(self.handleThreadException)
          
    except Exception as exception:
      self.handleThreadException(str(exception))

  def stop(self):

    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)
    
    self.deviceStatusLabel.setText('Статус устройства')

    if self.inputStreamType == 0:
      pass
    else:
      if self.ntripClientThread:
        self.ntripClientThread.kill()

  def exit(self):
    self.stop()
    self.close()

if __name__ == '__main__':

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
