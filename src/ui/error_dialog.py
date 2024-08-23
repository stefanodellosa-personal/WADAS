from PySide6.QtWidgets import QErrorMessage, QMessageBox

class ErrorMessage(QErrorMessage):
    def __init__(self, message):
        super(ErrorMessage, self).__init__()
        self.showMessage(message)
        self.setWindowTitle("Error")