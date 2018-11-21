from PyQt5.QtWidgets import QMessageBox

class Box(QMessageBox):

  def __init__(self, message):
    super(Box, self).__init__()
    self.setIcon(QMessageBox.Critical)
    self.setWindowTitle('Ошибка')
    self.setText(message)
