"""Module containing AI Model based logic (detection & classification)."""

import logging

import numpy as np
from PIL import Image
from PytorchWildlife.data import transforms as pw_trans

from wadas.ai.models import Classifier, OVMegaDetectorV5, txt_animalclasses

logger = logging.getLogger(__name__)


class DetectionPipeline:
    """Class containing AI Model functionalities (detection & classification)"""

    def __init__(self, device="auto", language="en"):
        self.device = device
        # Initializing the MegaDetectorV5 model for image detection
        logger.info("Initializing detection model to device %s...", self.device)
        self.detection_model = OVMegaDetectorV5(device=self.device)
        # Load classification model
        logger.info("Loading classification model to device %s...", self.device)
        self.classifier = Classifier(self.device)
        # Get the index of the animal class of the detection model
        self.animal_class_idx = next(
            key for key, value in self.detection_model.CLASS_NAMES.items() if value == "animal"
        )
        self.language = language

    def set_language(self, language):
        if language not in txt_animalclasses:
            raise ValueError("Language not supported")
        """Method to set the language for the classification labels."""
        self.language = language

    @staticmethod
    def check_models():
        """Method to check if models are initialized."""
        return OVMegaDetectorV5.check_model() and Classifier.check_model()

    @staticmethod
    def download_models(force: bool = False):
        """Method to check if models are initialized."""
        return OVMegaDetectorV5.download_model(force) and Classifier.download_model(force)

    def run_detection(self, img: Image, detection_treshold: float):
        """Method to run detection model on provided image."""

        img_array = np.array(img)

        # Initializing the Yolo-specific transform for the image
        transform = pw_trans.MegaDetector_v5_Transform(
            target_size=self.detection_model.IMAGE_SIZE,
            stride=self.detection_model.STRIDE,
        )

        # Performing the detection on the single image
        results = self.detection_model.single_image_detection(
            transform(img_array), img_array.shape, None, detection_treshold
        )

        # Checks for non animal in results and filter them out
        if results:
            # Get the index of the animal class
            animal_idx = np.where(results["detections"].class_id == self.animal_class_idx)
            # Filter out the non animal detections
            results["labels"] = [
                label
                for label, class_id in zip(results["labels"], results["detections"].class_id)
                if class_id == self.animal_class_idx
            ]
            results["detections"].xyxy = results["detections"].xyxy[animal_idx]
            results["detections"].confidence = results["detections"].confidence[animal_idx]
            results["detections"].class_id = results["detections"].class_id[animal_idx]

        return results

    def classify(self, img, results, classification_treshold):
        """Method to perform classification on detection result(s)."""

        if not results:
            return ""

        classification_id = 0
        classified_animals = []
        for xyxy in results["detections"].xyxy:
            # Cropping detection result(s) from original image leveraging detected boxes
            cropped_image = img.crop(xyxy)

            # Performing classification
            classification_result = self.classify_crop(cropped_image, classification_treshold)
            if classification_result[0]:

                classified_animals.append(
                    {
                        "id": classification_id,
                        "classification": classification_result,
                        "xyxy": xyxy,
                    }
                )
                classification_id += 1

        return classified_animals

    def classify_crop(self, crop_img, classification_treshold):
        """Classify animal on a crop (portion of original image)"""

        tensor_cropped = self.classifier.preprocessImage(crop_img)
        logits = self.classifier.predictOnBatch(tensor_cropped)[
            0,
        ]
        labels = txt_animalclasses[self.language]

        if max(logits) < classification_treshold:
            return ["", 0]

        return [labels[np.argmax(logits)], max(logits)]
