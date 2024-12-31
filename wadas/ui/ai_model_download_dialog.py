import os
import shutil
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QMessageBox
)
from huggingface_hub import hf_hub_download

from wadas.ui.qt.ui_ai_model_download import Ui_AiModelDownloadDialog


module_dir_path = os.path.dirname(os.path.abspath(__file__))

MODEL_FILES = [
    "detection_model.xml",
    "detection_model.bin",
    "classification_model.xml",
    "classification_model.bin"
]
REPO_ID = "alespalla/wadas"
SAVE_DIRECTORY = os.path.join(module_dir_path, "..", "..", "model")
MODEL_PATHS = [os.path.join(SAVE_DIRECTORY, f) for f in MODEL_FILES]

def download_and_move(repo_id, filename, token, target_directory):
    """Function to download and move files"""

    # Temporary download to the Hugging Face cache
    cached_file_path = hf_hub_download(repo_id=repo_id, filename=filename, use_auth_token=token)

    # Ensure the target directory exists
    os.makedirs(target_directory, exist_ok=True)

    target_file_path = os.path.join(target_directory, filename)

    # Move the file from the cache to the target directory
    shutil.move(cached_file_path, target_file_path)

    return target_file_path

class AiModelDownloadDialog(QDialog, Ui_AiModelDownloadDialog):
    """Class to implement AI model download dialog."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_AiModelDownloadDialog()
        self.setWindowTitle("Download AI Models")
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))

        self.stop_flag = False
        self.download_success = False

        self.ui.setupUi(self)
        self.ui.progressBar.setRange(0, len(MODEL_FILES))
        self.ui.progressBar.setEnabled(False)
        self.ui.pushButton_download.setEnabled(False)
        self.ui.lineEdit_token.textChanged.connect(self.validate)
        self.ui.pushButton_download.clicked.connect(self.download_models)
        self.ui.pushButton_cancel.clicked.connect(self.cancel_download)

    def download_models(self):
        """Method to trigger the model download"""
        #TODO: move this into separate thread

        self.ui.progressBar.setEnabled(True)
        self.ui.pushButton_download.setEnabled(False)

        token = self.ui.lineEdit_token.text().strip()
        if not token:
            QMessageBox.critical(self, "Error", "Token field cannot be empty.")
            return

        self.ui.progressBar.setValue(0)
        self.stop_flag = False
        for i, file_name in enumerate(MODEL_FILES):
            if self.stop_flag:
                QMessageBox.information(self, "Cancelled by the user", "Download cancelled by user.")
                return
            try:
                download_and_move(REPO_ID, file_name, token, SAVE_DIRECTORY)
                self.ui.progressBar.setValue(i + 1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error happened while downloading {file_name}: {str(e)}")
                self.ui.pushButton_download.setEnabled(True)
                return

        QMessageBox.information(self, "Success!", "All model files have been successfully downloaded.")
        self.download_success = True
        self.accept()

    def cancel_download(self):
        """Method to cancel Ai Model download"""
        self.stop_flag = True
        self.reject()

    def validate(self):
        """Method to validate the dialog input fields"""

        if self.ui.lineEdit_token.text():
            self.ui.pushButton_download.setEnabled(True)
        else:
            self.ui.pushButton_download.setEnabled(False)