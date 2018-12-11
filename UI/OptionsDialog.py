from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QDialogButtonBox, QMessageBox
from logic.config import Config

class OptionsDialog(QDialog):

  rowsCount = 0
  
  def __init__(self, configFilePath, title):

    super().__init__()

    self.config = Config(configFilePath)
    self.setWindowTitle(title)

    self.grid = QGridLayout()
    self.grid.setSpacing(10)
    self.setLayout(self.grid)

  def addRow(self, labelText, editObject):
    self.grid.addWidget(QLabel(labelText), self.rowsCount, 0)
    self.grid.addWidget(editObject, self.rowsCount, 1)
    self.rowsCount += 1

  def addButtonBox(self):
    buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    buttonBox.rejected.connect(self.reject)
    buttonBox.accepted.connect(self.accept)
    self.grid.addWidget(buttonBox, self.rowsCount, 0, 1, 0)

  def accept(self):
    try:
      self.config.save(self.serialize())
      super().accept()
    except Exception as e:
      QMessageBox.critical(self, 'Ошибка', str(e))
