"""QTextEdit module."""

import logging

from PySide6 import QtGui
from PySide6.QtCore import QObject, Signal


class QTextEditLogger(logging.Handler):
    """Class to enable logging in QTextEdit widget within mainwindow"""

    class Emitter(QObject):
        log = Signal(str)

    def __init__(self, parent):
        super().__init__()
        self.widget = parent
        self.widget.setReadOnly(True)
        self.widget.ensureCursorVisible()
        self.widget.moveCursor(QtGui.QTextCursor.End)

        self.emitter = QTextEditLogger.Emitter()
        self.emitter.log.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.emitter.log.emit(msg)
