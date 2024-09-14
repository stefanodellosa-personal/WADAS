"""Module containing AI Model based logic (detection & classification)."""

import os
import logging
import datetime
import requests
import cv2
from PIL import Image
import numpy as np
from PytorchWildlife.models import detection as pw_detection
from PytorchWildlife.data import transforms as pw_trans
#import intel_npu_acceleration_library as npu_lib
from PytorchWildlife import utils as pw_utils
from domain.classify_detections import Classifier, txt_animalclasses

logger = logging.getLogger(__name__)

def get_timestamp():
    """Method to prepare timestamp string to apply to images naming"""

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return timestamp

class AiModel():
    """Class containing AI Model functionalities (detection & classification)"""

    # Setting the device to use for computations ('cuda' indicates GPU, "npu" indicates intel NPU)
    #TODO: uncomment this: DEVICE = "npu" if npu_lib.backend.npu_available() else
    # "cuda" if torch.cuda.is_available() else "cpu"
    DEVICE = "cpu"
    CLASSIFICATION_MODEL = os.path.join("C:/", "Users/", "stefa/", "Downloads",
                                        "deepfaune-vit_large_patch14_dinov2.lvd142m.pt")

    def __init__(self):
        # Initializing the MegaDetectorV5 model for image detection
        logger.info("Initializing MegaDetectorV5 model for image detection to device {%s}...",
                     AiModel.DEVICE)
        self.detection_model = pw_detection.MegaDetectorV5(
            device=AiModel.DEVICE, pretrained=True)
        self.original_image = ""
        self.classification_treshold = 0.5
        self.detection_teshold = 0.5

        # Load classification model
        self.classifier = Classifier(AiModel.CLASSIFICATION_MODEL, AiModel.DEVICE)
        # Create required output folders
        os.makedirs("detection_output", exist_ok=True)
        os.makedirs("classification_output", exist_ok=True)
        os.makedirs("wadas_motion_detection", exist_ok=True)

    def process_image(self, img_path, save_detection_image: bool):
        """Method to run detection model on provided image."""

        if not os.path.isfile(img_path):
            logger.error("%s is not a valid image path. Aborting." % img_path)
            return

        logger.info("Running detection on image %s ...", img_path)
        img = Image.open(img_path).convert("RGB")
        img_array = np.array(img)
        img_array.shape, img_array.dtype

        # Initializing the Yolo-specific transform for the image
        transform = pw_trans.MegaDetector_v5_Transform(target_size=self.detection_model.IMAGE_SIZE,
                                                       stride=self.detection_model.STRIDE)

        # Performing the detection on the single image
        results = self.detection_model.single_image_detection(transform(img_array),
                                                              img_array.shape, img_path)
        detected_img_path = ""
        if len(results["detections"].xyxy) > 0 and save_detection_image:
            # Saving the detection results
            logger.info("Saving detection results...")
            pw_utils.save_detection_images(results, os.path.join(".","detection_output"),
                                           overwrite=False)
            detected_img_path = os.path.join("detection_output",  os.path.basename(img_path))
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
        img_path = os.path.join("url_imgs", "image_"+str(img_id)+"_"+
                                str(get_timestamp())+".jpg")
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
        classification_id = 0
        classified_animals = []
        for xyxy in results["detections"].xyxy:
            # Cropping detection result(s) from original image leveraging detected boxes
            cropped_image = img.crop(xyxy)
            cropped_image_path = os.path.join("classification_output", 
                                              str(classification_id)+'_cropped_image.jpg')
            cropped_image.save(cropped_image_path)
            logger.debug("Saved crop of image at %s.", cropped_image_path)
            # Performing classification
            classification_result = self.classify_crop(cropped_image)
            logger.info("Classification result: %s", classification_result)

            classified_animals.append({"id": classification_id,
                                    "classification": classification_result,
                                    "xyxy": xyxy})
            classification_id = classification_id+1

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
            animal["classification"][1] = round(animal["classification"][1], 2)

            # Draw black background rectangle to improve text readability. 
            # Replicating Megadetector settings whenever possible.
            text = str(animal["classification"][0])+ " "+str(animal["classification"][1])
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_scale = 1.5
            text_thickness = 2
            text_padding = 10

            text_x = x1 + text_padding
            text_y = y1 - text_padding
            text_width, text_height = cv2.getTextSize(text, font, text_scale, text_thickness,)[0]

            # Text background size is dependent on the size of the text
            text_background_x1 = x1
            text_background_y1 = y1 - 2 * text_padding - text_height
            text_background_x2 = x1 + 2 * text_padding + text_width
            text_background_y2 = y1

            classified_image = cv2.rectangle(classified_image,
                                             (text_background_x1, text_background_y1),
                                             (text_background_x2, text_background_y2),
                                              color,
                                              cv2.FILLED)

            # Add label to classification rectangle
            cv2.putText(classified_image, text, (text_x, text_y),
                        font, text_scale, (0,0,0), text_thickness, cv2.LINE_AA)
            cimg = Image.fromarray(classified_image)

            # Save classified image
            detected_img_name = os.path.basename(img_path)
            classified_img_name = "classified_"+detected_img_name
            classified_image_path = os.path.join("classification_output",classified_img_name)
            cimg.save(classified_image_path)
        return classified_image_path

    def classify_crop(self, PIL_crop):
        """Classify animal on a crop (portion of original image)"""

        classifications = self.get_classifications(PIL_crop)
        classified_animal = ['', 0]
        for result in classifications:
            if result[1] > classified_animal[1]:
                classified_animal = result

        return classified_animal

    """ This code snipped is created by EcoAssist team. Orignal license is shown below.
     Source: https://github.com/PetervanLunteren/EcoAssist/blob/main/classification_utils/model_types/deepfaune/classify_detections.py
     The code is unaltered, except for three adjustments:
     1- function rename,
     2- function is now a method of AiModel class,
     3- classifier object from AiModel attributes.  """

    ##############################################
    ############## ECOASSIST START ###############
    ##############################################

    """Copyright (c) 2022 Peter van Lunteren

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE."""

    # predict from cropped image
    # input: cropped PIL image
    # output: unsorted classifications formatted as [['aardwolf', 2.3025326090220233e-09], ['african wild cat', 5.658252888451898e-08], ... ]
    # no need to remove forbidden classes from the predictions, that will happen in infrence_lib.py
    # this is also the place to preprocess the image if that need to happen

    # def get_classification(PIL_crop):
    # ADJUSTMENT 1
    def get_classifications(self, PIL_crop): # ADJUSTMENT 2
        tensor_cropped = self.classifier.preprocessImage(PIL_crop) #ADJUSTMENT 3
        confs = self.classifier.predictOnBatch(tensor_cropped)[0,] #ADJUSTMENT 3
        lbls = txt_animalclasses['en']
        classifications = []
        for i in range(len(confs)):
            classifications.append([lbls[i], confs[i]])
        return classifications

    ##############################################
    ############### ECOASSIST END ################
    ##############################################
