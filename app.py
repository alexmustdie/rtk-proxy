#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from UI.BaseStationOptionsDialog import BaseStationOptionsDialog
from UI.NtripOptionsDialog import NtripOptionsDialog
from UI.AutopilotOptionsDialog import AutopilotOptionsDialog
from UI.ModemOptionsDialog import ModemOptionsDialog

from logic.BaseStation import BaseStation
from logic.Ntrip import Ntrip

from logic.Output import Autopilot, Modem

class MainWindow(QWidget):

  deviceStatusLabelDefaultText = 'Статус устройства'

  inputClientType = 0
  inputClientOptions = None
  inputClientThread = None

  outputClientType = 0
  outputClientOptions = None

  def __init__(self):

    super(MainWindow, self).__init__()

    try:
      self.inputClientOptions = BaseStationOptionsDialog().serialize()
      self.outputClientOptions = AutopilotOptionsDialog().serialize()
    except:
      pass

    grid = QGridLayout()
    grid.setSpacing(10)

    # 1 row

    streamTitleLabel = QLabel('Поток')
    grid.addWidget(streamTitleLabel, 0, 0)

    typeTitleLabel = QLabel('Тип клиента')
    grid.addWidget(typeTitleLabel, 0, 1)

    optionsTitleLabel = QLabel('Опции')
    grid.addWidget(optionsTitleLabel, 0, 2)

    bytesTitleLabel = QLabel('Байты')
    grid.addWidget(bytesTitleLabel, 0, 3)

    for widget in (streamTitleLabel, typeTitleLabel, optionsTitleLabel, bytesTitleLabel):
      widget.setStyleSheet("padding:5;background-color:lightgray;")
      widget.setAlignment(Qt.AlignCenter)

    # 2 row

    grid.addWidget(QLabel('Вход'), 1, 0)
    
    inputClientTypeComboBox = QComboBox()
    inputClientTypeComboBox.addItems(['Базовая станция', 'NTRIP'])
    inputClientTypeComboBox.currentIndexChanged.connect(self.onInputClientTypeChanged)
    grid.addWidget(inputClientTypeComboBox, 1, 1)

    inputClientOptionsButton = QPushButton('...')
    inputClientOptionsButton.clicked.connect(self.showInputClientOptions)
    grid.addWidget(inputClientOptionsButton, 1, 2)

    self.inputClientBytesCountLabel = QLabel('0')
    self.inputClientBytesCountLabel.setAlignment(Qt.AlignRight)
    grid.addWidget(self.inputClientBytesCountLabel, 1, 3)

    # 3 row

    grid.addWidget(QLabel('Выход'), 2, 0)
    
    outputClientTypeComboBox = QComboBox()
    outputClientTypeComboBox.addItems(['Автопилот', 'Модем'])
    outputClientTypeComboBox.currentIndexChanged.connect(self.onOutputClientTypeChanged)
    grid.addWidget(outputClientTypeComboBox, 2, 1)
    
    outputClientOptionsButton = QPushButton('...')
    outputClientOptionsButton.clicked.connect(self.showOutputClientOptions)
    grid.addWidget(outputClientOptionsButton, 2, 2)

    self.outputClientBytesCountLabel = QLabel('0')
    self.outputClientBytesCountLabel.setAlignment(Qt.AlignRight)
    grid.addWidget(self.outputClientBytesCountLabel, 2, 3)

    # 4 row

    self.deviceStatusLabel = QLabel(self.deviceStatusLabelDefaultText)
    self.deviceStatusLabel.setStyleSheet("padding:5;background-color:lightgray;")
    self.deviceStatusLabel.setWordWrap(True)
    self.deviceStatusLabel.setFixedSize(400, 45)
    grid.addWidget(self.deviceStatusLabel, 3, 0, 1, 4)

    # 5 row

    self.startButton = QPushButton('Запустить')
    self.startButton.clicked.connect(self.start)
    grid.addWidget(self.startButton, 4, 0)

    self.stopButton = QPushButton('Остановить')
    self.stopButton.setDisabled(True)
    self.stopButton.clicked.connect(self.stop)
    grid.addWidget(self.stopButton, 4, 1)

    exitButton = QPushButton('Выйти')
    exitButton.clicked.connect(self.exit)
    grid.addWidget(exitButton, 4, 3)

    # rows end
    
    self.setLayout(grid)
    self.setFixedSize(420, 0)
    self.setWindowTitle('RTK proxy')

  def onInputClientTypeChanged(self, index):
    self.inputClientType = index
    self.inputClientOptions = BaseStationOptionsDialog().serialize() if self.inputClientType == 0 else NtripOptionsDialog().serialize()

  def showInputClientOptions(self):
    dialog = BaseStationOptionsDialog() if self.inputClientType == 0 else NtripOptionsDialog()
    if dialog.exec_() == QDialog.Accepted:
      self.inputClientOptions = dialog.serialize()

  def onOutputClientTypeChanged(self, index):
    self.outputClientType = index
    self.outputClientOptions = AutopilotOptionsDialog().serialize() if self.outputClientType == 0 else ModemOptionsDialog().serialize()

  def showOutputClientOptions(self):
    dialog = AutopilotOptionsDialog() if self.outputClientType == 0 else ModemOptionsDialog()
    if dialog.exec_() == QDialog.Accepted:
      self.outputClientOptions = dialog.serialize()

  def updateDeviceStatus(self, status):
    self.deviceStatusLabel.setText(status)

  def updateBytesCount(self, bytesCount):
    bytesCount = '{:,}'.format(bytesCount)
    self.inputClientBytesCountLabel.setText(bytesCount)
    self.outputClientBytesCountLabel.setText(bytesCount)

  def handleThreadException(self, e):
    QMessageBox.critical(self, 'Ошибка', str(e))
    self.stop()

  def start(self):

    self.startButton.setEnabled(False)
    self.stopButton.setEnabled(True)

    try:

      if self.outputClientOptions:
        if self.outputClientType == 0:
          outputClientStream = Autopilot(**self.outputClientOptions)
        else:
          outputClientStream = Modem(**self.outputClientOptions)
      else:
        raise Exception('Настройте опции выходного потока')

      if self.inputClientOptions:
        if self.inputClientType == 0:
          self.inputClientThread = BaseStation.Thread(self.inputClientOptions, outputClientStream)
        else:
          self.inputClientThread = Ntrip.Thread(self.inputClientOptions, outputClientStream)
      else:
        raise Exception('Настройте опции входного потока')

      self.inputClientThread.deviceStatus.connect(self.updateDeviceStatus)
      self.inputClientThread.bytesCount.connect(self.updateBytesCount)
      self.inputClientThread.failed.connect(self.handleThreadException)
      self.inputClientThread.start()

    except Exception as e:
      self.handleThreadException(e)

  def stop(self):

    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)
    self.deviceStatusLabel.setText(self.deviceStatusLabelDefaultText)
    
    if self.inputClientThread:
      self.inputClientThread.kill()

  def exit(self):
    self.stop()
    self.close()

if __name__ == '__main__':

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
