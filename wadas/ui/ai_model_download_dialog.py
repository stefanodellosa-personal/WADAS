import os
import shutil
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QMessageBox
)
from huggingface_hub import hf_hub_download


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

def check_model_files(model_paths):
    """Function to check if all AI model files exist"""

    return all(os.path.isfile(path) for path in model_paths)

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

class AiModelDownloadDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download AI Models")
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.setLayout(QVBoxLayout())

        self.model_files = MODEL_FILES
        self.repo_id = REPO_ID
        self.save_directory = SAVE_DIRECTORY
        self.stop_flag = [False]
        self.download_success = False

        self.label = QLabel("Insert your Hugging Face access token:")
        self.layout().addWidget(self.label)

        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)
        self.layout().addWidget(self.token_input)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len(self.model_files))
        self.layout().addWidget(self.progress_bar)

        self.download_button = QPushButton("Download Models")
        self.download_button.clicked.connect(self.download_models)
        self.layout().addWidget(self.download_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.layout().addWidget(self.cancel_button)

    def download_models(self):
        token = self.token_input.text().strip()
        if not token:
            QMessageBox.critical(self, "Error", "Token field cannot be empty.")
            return

        self.progress_bar.setValue(0)
        self.stop_flag[0] = False
        for i, file_name in enumerate(self.model_files):
            if self.stop_flag[0]:
                QMessageBox.information(self, "Cancelled by the user", "Download cancelled by user.")
                return
            try:
                download_and_move(self.repo_id, file_name, token, self.save_directory)
                self.progress_bar.setValue(i + 1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error happened while downloading {file_name}: {str(e)}")
                return

        QMessageBox.information(self, "Success!", "All model files have been successfully downloaded.")
        self.download_success = True
        self.accept()

    def cancel_download(self):
        self.stop_flag[0] = True
