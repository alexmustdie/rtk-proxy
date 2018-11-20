#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import queue

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from dialogs import autopilot, baseStation, NTRIP
from proxy.NtripClient import NtripClientThread

class MainWindow(QWidget):

  # TODO: сделать индикацию, кнопку остановки и выбор COM-порта

  def __init__(self):
    
    super(MainWindow, self).__init__()

    self.inputStreamType = 0

    self.baseStationThread = None
    self.ntripClientThread = None

    self.baseStationOptions = baseStation.Options().serialize()
    self.ntripOptions = NTRIP.Options().serialize()
    self.autopilotOptions = autopilot.Options().serialize()

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

    self.startButton = QPushButton('Запустить')
    self.startButton.clicked.connect(self.start)
    grid.addWidget(self.startButton, 3, 0)

    self.stopButton = QPushButton('Остановить')
    self.stopButton.setDisabled(True)
    self.stopButton.clicked.connect(self.stop)
    grid.addWidget(self.stopButton, 3, 1)

    exitButton = QPushButton('Выйти')
    exitButton.clicked.connect(self.exit)
    grid.addWidget(exitButton, 3, 2)
    
    self.setLayout(grid)
    self.setGeometry(300, 300, 0, 0)
    self.setFixedSize(0, 0)
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

  def showAlertBox(self, text):
    alertBox = QMessageBox()
    alertBox.setIcon(QMessageBox.Critical)
    alertBox.setWindowTitle('Ошибка')
    alertBox.setText(text)
    alertBox.exec_()

  def start(self):

    self.startButton.setEnabled(False)
    self.stopButton.setDisabled(False)

    try:

      if self.inputStreamType == 0:
        pass
      else:
        bucket = queue.Queue()
        self.ntripClientThread = NtripClientThread(bucket, self.ntripOptions, self.autopilotOptions)
        self.ntripClientThread.start()

        while True:
          try:
            exc = bucket.get(block=False)
          except queue.Empty:
            pass
          else:
            raise exc[1]

          self.ntripClientThread.join(0.1)

          if self.ntripClientThread.isAlive():
            continue
          else:
            break
          
    except Exception as e:
      self.showAlertBox(str(e))
      self.stop()

  def stop(self):
    
    self.startButton.setEnabled(True)
    self.stopButton.setDisabled(True)

    if self.inputStreamType == 0:
      pass
    else:
      if self.ntripClientThread: self.ntripClientThread.kill()

  def exit(self):
    self.stop()
    self.close()

if __name__ == '__main__':

  app = QApplication(sys.argv)

  window = MainWindow()
  window.show()

  sys.exit(app.exec_())
