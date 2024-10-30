"""Module containing AI Model based logic (detection & classification)."""

import logging
import os

import cv2
import numpy as np
import requests
from PIL import Image
from PytorchWildlife import utils as pw_utils

from ai import DetectionPipeline
from domain.utils import get_timestamp

logger = logging.getLogger(__name__)


class AiModel:
    """Class containing AI Model functionalities (detection & classification)"""

    DEVICE = "auto"
    classification_treshold = 0.5
    detection_treshold = 0.5
    language = "en"

    def __init__(self):
        # Initializing the MegaDetectorV5 model for image detection
        logger.info(
            "Initializing AI model for image detection and classification to %s...", AiModel.DEVICE
        )
        self.detection_pipeline = DetectionPipeline(
            device=AiModel.DEVICE, language=AiModel.language
        )

        self.original_image = ""

        # Create required output folders
        os.makedirs("detection_output", exist_ok=True)
        os.makedirs("classification_output", exist_ok=True)
        os.makedirs("wadas_motion_detection", exist_ok=True)

        logger.debug(
            "Detection treshold: %s, Classification treshod: %s.",
            self.detection_treshold,
            self.classification_treshold,
        )

    @staticmethod
    def check_model():
        """Method to check if model is initialized."""
        return DetectionPipeline.check_models()

    @staticmethod
    def download_models():
        """Method to check if model is initialized."""
        return DetectionPipeline.download_models()

    def process_image(self, img_path, save_detection_image: bool):
        """Method to run detection model on provided image."""

        if not os.path.isfile(img_path):
            logger.error("%s is not a valid image path. Aborting.", img_path)
            return

        logger.info("Running detection on image %s ...", img_path)
        img = Image.open(img_path).convert("RGB")
        results = self.detection_pipeline.run_detection(img, AiModel.detection_treshold)

        detected_img_path = ""
        if len(results["detections"].xyxy) > 0 and save_detection_image:
            # Saving the detection results
            logger.info("Saving detection results...")
            results["img_id"] = img_path
            pw_utils.save_detection_images(
                results, os.path.join(".", "detection_output"), overwrite=False
            )
            detected_img_path = os.path.join("detection_output", os.path.basename(img_path))
        else:
            logger.info("No detected animals for %s. Removing image.", img_path)
            os.remove(img_path)

        return results, detected_img_path

    def process_image_from_url(self, url, img_id, save_detection_image):
        """Method to run detection model on image provided by URL"""

        logger.info("Processing image from url: %s", url)
        # Opening the image from url
        img = Image.open(requests.get(url, stream=True).raw).convert("RGB")

        # Save image to disk
        os.makedirs("url_imgs", exist_ok=True)
        img_path = os.path.join(
            "url_imgs", "image_" + str(img_id) + "_" + str(get_timestamp()) + ".jpg"
        )
        img.save(img_path)
        logger.info("Saved processed image at: %s", img_path)

        results, detected_img_path = self.process_image(img_path, save_detection_image)
        return [img_path, results, detected_img_path]

    def classify(self, img_path, results):
        """Method to perform classification on detection result(s)."""

        if not results:
            logger.warning("No results to classify. Skipping classification.")
            return ""

        logger.info("Running classification on %s image...", img_path)
        img = Image.open(img_path).convert("RGB")

        classified_animals = self.detection_pipeline.classify(
            img, results, AiModel.classification_treshold
        )

        for detection in classified_animals:
            # Cropping detection result(s) from original image leveraging detected boxes
            cropped_image = img.crop(detection["xyxy"])
            cropped_image_path = os.path.join(
                "classification_output", f"{detection['id']}_cropped_image.jpg"
            )
            cropped_image.save(cropped_image_path)
            logger.debug("Saved crop of image at %s.", cropped_image_path)

        img_path = self.build_classification_square(img, classified_animals, img_path)
        return img_path, classified_animals

    def build_classification_square(self, img, classified_animals, img_path):
        """Build square on classified animals."""

        classified_image_path = ""
        # Build classification square
        orig_image = np.array(img)
        for animal in classified_animals:
            # Classification box attributes
            x1 = int(animal["xyxy"][0])
            y1 = int(animal["xyxy"][1])
            x2 = int(animal["xyxy"][2])
            y2 = int(animal["xyxy"][3])
            color = (255, 0, 0)
            classified_image = cv2.rectangle(orig_image, (x1, y1), (x2, y2), color, 2)

            # Round precision on classification score
            animal["classification"][1] = round(animal["classification"][1].item(), 2)

            # Draw black background rectangle to improve text readability.
            # Replicating Megadetector settings whenever possible.
            text = str(animal["classification"][0]) + " " + str(animal["classification"][1])
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_scale = 1.5
            text_thickness = 2
            text_padding = 10

            text_x = x1 + text_padding
            text_y = y1 - text_padding
            text_width, text_height = cv2.getTextSize(
                text,
                font,
                text_scale,
                text_thickness,
            )[0]

            # Text background size is dependent on the size of the text
            text_background_x1 = x1
            text_background_y1 = y1 - 2 * text_padding - text_height
            text_background_x2 = x1 + 2 * text_padding + text_width
            text_background_y2 = y1

            classified_image = cv2.rectangle(
                classified_image,
                (text_background_x1, text_background_y1),
                (text_background_x2, text_background_y2),
                color,
                cv2.FILLED,
            )

            # Add label to classification rectangle
            cv2.putText(
                classified_image,
                text,
                (text_x, text_y),
                font,
                text_scale,
                (0, 0, 0),
                text_thickness,
                cv2.LINE_AA,
            )
            cimg = Image.fromarray(classified_image)

            # Save classified image
            detected_img_name = os.path.basename(img_path)
            classified_img_name = "classified_" + detected_img_name
            classified_image_path = os.path.join("classification_output", classified_img_name)
            cimg.save(classified_image_path)
        return classified_image_path
