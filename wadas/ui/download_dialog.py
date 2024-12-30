# This file is part of WADAS project.
#
# WADAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WADAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WADAS. If not, see <https://www.gnu.org/licenses/>.
#
# Author(s): Stefano Dell'Osa, Alessandro Palla, Cesare Di Mauro, Antonio Farina
# Date: 2024-08-14
# Description: UI file download UI dialog

import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog

from wadas.domain.download_file import Downloader
from wadas.ui.qt.ui_download_file import Ui_DialogDownloadFile


class DownloadDialog(QDialog, Ui_DialogDownloadFile):
    def __init__(self, url, filename):
        super().__init__()
        self.ui = Ui_DialogDownloadFile()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), "img", "mainwindow_icon.jpg")))
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
