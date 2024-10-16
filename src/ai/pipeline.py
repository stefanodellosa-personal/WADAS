"""Module containing AI Model based logic (detection & classification)."""

import numpy as np
from PIL import Image
from PytorchWildlife.data import transforms as pw_trans

from ai.models import OVMegaDetectorV5, Classifier, txt_animalclasses
import logging

logger = logging.getLogger(__name__)


class DetectionPipeline:
    """Class containing AI Model functionalities (detection & classification)"""

    def __init__(self, device="cpu"):
        self.device = device
        # Initializing the MegaDetectorV5 model for image detection
        logger.info(f"Initializing detection model to device {self.device}...")
        self.detection_model = OVMegaDetectorV5(device=self.device)
        # Load classification model
        logger.info(f"Loading classification model to device {self.device}...")
        self.classifier = Classifier(self.device)

    def run_detection(self, img: Image, detection_treshold: float):
        """Method to run detection model on provided image."""

        img_array = np.array(img)
        img_array.shape, img_array.dtype

        # Initializing the Yolo-specific transform for the image
        transform = pw_trans.MegaDetector_v5_Transform(
            target_size=self.detection_model.IMAGE_SIZE,
            stride=self.detection_model.STRIDE,
        )

        # Performing the detection on the single image
        results = self.detection_model.single_image_detection(
            transform(img_array), img_array.shape, None, detection_treshold
        )

        # Checks for humans in results
        if (
            results
            and results["labels"]
            and "person" in results["labels"][0]
            and len(results["labels"]) == 1
        ):
            return None

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
            classification_result = self.classify_crop(
                cropped_image, classification_treshold
            )
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

    def classify_crop(self, crop_img, classification_treshold, language="en"):
        """Classify animal on a crop (portion of original image)"""

        tensor_cropped = self.classifier.preprocessImage(crop_img)
        logits = self.classifier.predictOnBatch(tensor_cropped)[
            0,
        ]
        labels = txt_animalclasses[language]

        if max(logits) < classification_treshold:
            return ["", 0]

        return [labels[np.argmax(logits)], max(logits)]
