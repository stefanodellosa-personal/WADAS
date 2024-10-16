"""Download Dialog Module"""

import os

from PySide6.QtWidgets import QDialog, QLabel, QPushButton
from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QIcon

from domain.download_file import Downloader
from ui.ui_download_file import Ui_DialogDownloadFile


class DownloadDialog(QDialog, Ui_DialogDownloadFile):
    def __init__(self, url, filename):
        super().__init__()
        self.ui = Ui_DialogDownloadFile()
        self.ui.setupUi(self)
        self.setWindowIcon(
            QIcon(os.path.join(os.getcwd(), "img", "mainwindow_icon.jpg"))
        )
        self.ui.pushButton_cancel.setEnabled(False)
        # Slots
        self.ui.pushButton_download.pressed.connect(self.initDownload)
        self.ui.pushButton_cancel.pressed.connect(self.cancel)

        self.url = url
        self.filename = filename

    def initDownload(self):
        """Method to init the download UI."""
        self.ui.label.setText("Downloading file...")
        # Disable the button while the file is downloading.
        self.ui.pushButton_download.setEnabled(False)
        self.ui.pushButton_cancel.setEnabled(True)
        # Run the download in a new thread.
        self.downloader = Downloader(self.url, self.filename)

        # Connect the signals which send information about the download
        # progress with the proper methods of the progress bar.
        self.downloader.setTotalProgress.connect(self.ui.progressBar.setMaximum)
        self.downloader.setCurrentProgress.connect(self.ui.progressBar.setValue)
        # Qt will invoke the `succeeded()` method when the file has been
        # downloaded successfully and `downloadFinished()` when the
        # child thread finishes.
        self.downloader.succeeded.connect(self.downloadSucceeded)
        self.downloader.finished.connect(self.downloadFinished)
        self.downloader.start()

    def downloadSucceeded(self):
        # Set the progress at 100%.
        self.ui.progressBar.setValue(self.ui.progressBar.maximum())
        self.ui.label.setText("Download completed!")

    def downloadFinished(self):
        # Restore the buttons.
        self.ui.pushButton_download.setEnabled(True)
        self.ui.pushButton_cancel.setEnabled(False)
        # Delete the thread.
        del self.downloader
        self.close()

    def cancel(self):
        """Method to cancel download operation."""
        self.ui.pushButton_download.setEnabled(True)
        self.ui.pushButton_cancel.setEnabled(False)
        self.downloader.abort()
        del self.downloader
