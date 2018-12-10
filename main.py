#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from UI.BaseStationOptionsDialog import BaseStationOptionsDialog
from UI.NtripOptionsDialog import NtripOptionsDialog
from UI.AutopilotOptionsDialog import AutopilotOptionsDialog

from logic.BaseStation import BaseStation
from logic.Ntrip import Ntrip

class MainWindow(QWidget):

  deviceStatusLabelDefaultText = 'Статус устройства'

  inputClientType = 0
  inputClientThread = None

  def __init__(self):

    super(MainWindow, self).__init__()

    self.baseStationOptions = BaseStationOptionsDialog().serialize()
    self.ntripOptions = NtripOptionsDialog().serialize()
    self.autopilotOptions = AutopilotOptionsDialog().serialize()

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
      widget.setStyleSheet("padding:5;background-color:lightgray;");
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
    grid.addWidget(QLabel('Aвтопилот'), 2, 1)
    
    outputClientOptionsButton = QPushButton('...')
    outputClientOptionsButton.clicked.connect(self.showOutputClientOptions)
    grid.addWidget(outputClientOptionsButton, 2, 2)

    self.outputClientBytesCountLabel = QLabel('0')
    self.outputClientBytesCountLabel.setAlignment(Qt.AlignRight)
    grid.addWidget(self.outputClientBytesCountLabel, 2, 3)

    # 4 row

    self.deviceStatusLabel = QLabel(self.deviceStatusLabelDefaultText)
    self.deviceStatusLabel.setStyleSheet("padding:5;background-color:lightgray;");
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

  def showInputClientOptions(self):
    if self.inputClientType == 0:
      dialog = BaseStationOptionsDialog()
      if (dialog.exec_() == QDialog.Accepted):
        self.baseStationOptions = dialog.serialize()
    else:
      dialog = NtripOptionsDialog()
      if (dialog.exec_() == QDialog.Accepted):
        self.ntripOptions = dialog.serialize()

  def showOutputClientOptions(self):
    dialog = AutopilotOptionsDialog()
    if (dialog.exec_() == QDialog.Accepted):
      self.autopilotOptions = dialog.serialize()

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

      if self.inputClientType == 0:
        self.inputClientThread = BaseStation.Thread(self.baseStationOptions, self.autopilotOptions)
      else:
        self.inputClientThread = Ntrip.Thread(self.ntripOptions, self.autopilotOptions)

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
