"""Module to download a file from URL."""

import os

from urllib.request import urlopen

from PySide6.QtCore import Signal, QThread


class Downloader(QThread):
    """Class to handle file download in dedicated QThread"""
    # Signal for to establish the maximum value of the progress bar.
    setTotalProgress = Signal(int)
    # Signal to increase the progress.
    setCurrentProgress = Signal(int)
    # Signal to be emitted once file has been downloaded successfully.
    succeeded = Signal()

    def __init__(self, url, filename):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        """Method to trigger the download of the file."""

        readBytes = 0
        chunkSize = 1024
        # Open the URL address.
        with urlopen(self.url) as r:
            # Tell the window the amount of bytes to be downloaded.
            self.setTotalProgress.emit(int(r.info()["Content-Length"]))
            with open(self.filename, "ab") as f:
                while True:
                    # Read a piece of the file we are downloading.
                    chunk = r.read(chunkSize)
                    # If the result is `None`, that means data is not fully downloaded yet.
                    if chunk is None:
                        continue
                    # If the result is an empty `bytes` instance, then the download is complete.
                    elif chunk == b"":
                        break
                    # Write into the local file the downloaded chunk.
                    f.write(chunk)
                    readBytes += chunkSize
                    # Tell the window how many bytes we have received.
                    self.setCurrentProgress.emit(readBytes)
        self.succeeded.emit()

    def abort(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)
