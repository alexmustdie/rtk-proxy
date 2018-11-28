from PyQt5.QtWidgets import QMessageBox

class AlertBox(QMessageBox):

  def __init__(self, message):
    super().__init__()
    self.setIcon(QMessageBox.Critical)
    self.setWindowTitle('Ошибка')
    self.setText(message)
