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
# Date: 2024-10-11
# Description: This module implements OpenVINO related classes and functionalities.

from pathlib import Path

import numpy as np
import torch
from PytorchWildlife.data import transforms as pw_trans
from PytorchWildlife.models import detection as pw_detection
from torchvision.transforms import InterpolationMode, transforms

from wadas.ai.openvino_model import OVModel
from wadas.ai.ov_predictor import OVPredictor

txt_animalclasses = {
    "fr": [
        "blaireau",
        "bouquetin",
        "cerf",
        "chamois",
        "chat",
        "chevre",
        "chevreuil",
        "chien",
        "ecureuil",
        "equide",
        "genette",
        "herisson",
        "lagomorphe",
        "loup",
        "lynx",
        "marmotte",
        "micromammifere",
        "mouflon",
        "mouton",
        "mustelide",
        "oiseau",
        "ours",
        "ragondin",
        "renard",
        "sanglier",
        "vache",
    ],
    "en": [
        "badger",
        "ibex",
        "red deer",
        "chamois",
        "cat",
        "goat",
        "roe deer",
        "dog",
        "squirrel",
        "equid",
        "genet",
        "hedgehog",
        "lagomorph",
        "wolf",
        "lynx",
        "marmot",
        "micromammal",
        "mouflon",
        "sheep",
        "mustelid",
        "bird",
        "bear",
        "nutria",
        "fox",
        "wild boar",
        "cow",
    ],
    "it": [
        "tasso",
        "stambecco",
        "cervo",
        "camoscio",
        "gatto",
        "capra",
        "capriolo",
        "cane",
        "scoiattolo",
        "equide",
        "genet",
        "riccio",
        "lagomorfo",
        "lupo",
        "lince",
        "marmotta",
        "micromammifero",
        "muflone",
        "pecora",
        "mustelide",
        "uccello",
        "orso",
        "nutria",
        "volpe",
        "cinghiale",
        "mucca",
    ],
    "de": [
        "Dachs",
        "Steinbock",
        "Rothirsch",
        "Gämse",
        "Katze",
        "Ziege",
        "Rehwild",
        "Hund",
        "Eichhörnchen",
        "Equiden",
        "Ginsterkatze",
        "Igel",
        "Lagomorpha",
        "Wolf",
        "Luchs",
        "Murmeltier",
        "Kleinsäuger",
        "Mufflon",
        "Schaf",
        "Mustelide",
        "Vogen",
        "Bär",
        "Nutria",
        "Fuchs",
        "Wildschwein",
        "Kuh",
    ],
}


class OVMegaDetectorV5(pw_detection.MegaDetectorV5):
    """MegaDetectorV5 class for detection model"""

    def __init__(self, device):
        self.model = OVModel(
            Path("detection", "MDV5-yolov5_openvino_model", "MDV5-yolov5.xml"), device
        )
        self.device = "cpu"  # torch device, keep to CPU when using with OpenVINO

        self.transform = pw_trans.MegaDetector_v5_Transform(
            target_size=self.IMAGE_SIZE, stride=self.STRIDE
        )

    def get_class_names(self):
        """Get class names"""
        return self.CLASS_NAMES

    def run(self, img_array: np.ndarray, detection_threshold: float):
        """Run detection model"""
        return self.single_image_detection(img_array, None, detection_threshold, None)

    @staticmethod
    def check_model():
        """Check if detection model is initialized"""
        return OVModel.check_model(
            Path("detection", "MDV5-yolov5_openvino_model", "MDV5-yolov5.xml")
        )

    @staticmethod
    def download_model(force: bool = False):
        """Check if model is initialized"""
        return OVModel.download_model("detection_model", force)


class OVMegaDetectorV6(pw_detection.MegaDetectorV6):
    """MegaDetectorV6 class for detection model"""

    IMAGE_SIZE = 640

    def __init__(self, device):
        self.predictor = OVPredictor(ov_device=device)
        self.device = "cpu"  # torch device, keep to CPU when using with OpenVINO

        self.predictor.setup_model("MDV6b-yolov9c_openvino_model", verbose=False)

        self.predictor.args.imgsz = self.IMAGE_SIZE
        self.predictor.args.save = (
            False  # Will see if we want to use ultralytics native inference saving functions.
        )

    def get_class_names(self):
        """Get class names"""
        return self.CLASS_NAMES

    def run(self, img_array: np.ndarray, detection_threshold: float):
        """Run detection model"""
        return self.single_image_detection(img_array, None, detection_threshold, None)

    @staticmethod
    def check_model():
        """Check if detection model is initialized"""
        return OVModel.check_model("MDV6b-yolov9c_openvino_model")

    @staticmethod
    def download_model(force: bool = False):
        """Check if model is initialized"""
        return OVModel.download_model("MDV6b-yolov9c_openvino_model", force)


class Classifier:
    """Classifier class for classification model"""

    CROP_SIZE = 182

    def __init__(self, device):
        self.model = OVModel(Path("classification", "DFv1.2_openvino_model", "DFv1.2.xml"), device)
        self.transforms = transforms.Compose(
            [
                transforms.Resize(
                    size=(self.CROP_SIZE, self.CROP_SIZE),
                    interpolation=InterpolationMode.BICUBIC,
                    max_size=None,
                    antialias=None,
                ),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=torch.tensor([0.4850, 0.4560, 0.4060]),
                    std=torch.tensor([0.2290, 0.2240, 0.2250]),
                ),
            ]
        )

    @staticmethod
    def check_model():
        """Check if classification model is initialized"""
        return OVModel.check_model(Path("classification", "DFv1.2_openvino_model", "DFv1.2.xml"))

    @staticmethod
    def download_model(force: bool = False):
        """Download classification model"""
        return OVModel.download_model("classification_model", force)

    def predictOnBatch(self, batchtensor, withsoftmax=True):
        """Predict on a batch of images"""
        logits = self.model(batchtensor)
        return logits.softmax(dim=1) if withsoftmax else logits

    def preprocessImage(self, croppedimage):
        """Preprocess the image for classification
        The preprocessing consists of resizing, converting to tensor and normalizing the image.
        """
        preprocessimage = self.transforms(croppedimage)
        return preprocessimage.unsqueeze(dim=0)

    def predictOnImages(self, request, withsoftmax=True) -> torch.Tensor:
        img, results = request
        if results["detections"].xyxy.shape[0] == 0:
            return
        """Predict on a single image"""
        tensor = torch.concatenate(
            [self.preprocessImage(img.crop(xyxy)) for xyxy in results["detections"].xyxy],
            axis=0,
        )
        return self.predictOnBatch(tensor, withsoftmax=withsoftmax)
