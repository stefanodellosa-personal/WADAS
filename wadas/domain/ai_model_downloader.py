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
# Date: 2025-01-01
# Description: Module containing Ai Model downloader class and methods.

import logging
import os
import shutil

from huggingface_hub import hf_hub_download
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)
module_dir_path = os.path.dirname(os.path.abspath(__file__))

MODEL_FILES = [
    "detection_model.xml",
    "detection_model.bin",
    "classification_model.xml",
    "classification_model.bin",
]
REPO_ID = "wadas-it/wadas"
SAVE_DIRECTORY = os.path.join(module_dir_path, "..", "..", "model")
MODEL_PATHS = [os.path.join(SAVE_DIRECTORY, f) for f in MODEL_FILES]


class AiModelsDownloader(QObject):
    """Class implementing Ai Model download logic."""

    run_finished = Signal()
    run_progress = Signal(int)
    error_happened = Signal(str)

    def __init__(self, token):
        super(AiModelsDownloader, self).__init__()
        self.token = token
        self.stop_flag = False

    def run(self):
        """Ai Model Download running in a dedicated thread"""
        try:
            os.makedirs(SAVE_DIRECTORY, exist_ok=True)
            for i, file_name in enumerate(MODEL_FILES):
                if self.stop_flag:
                    break

                # Temporary download to the Hugging Face cache
                cached_file_path = hf_hub_download(
                    repo_id=REPO_ID, filename=file_name, use_auth_token=self.token
                )

                target_file_path = os.path.join(SAVE_DIRECTORY, file_name)

                # Move the file from the cache to the target directory
                shutil.move(cached_file_path, target_file_path)

                self.run_progress.emit((i + 1) * 100 // len(MODEL_FILES))
            self.run_finished.emit()
        except Exception as e:
            self.error_happened.emit(str(e))

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Dialog."""

        if self.thread().isInterruptionRequested():
            self.stop_flag = True
            logger.error("Ai Models download cancelled by user.")
