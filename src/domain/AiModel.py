from PytorchWildlife.models import detection as pw_detection
from PytorchWildlife.data import transforms as pw_trans
#import intel_npu_acceleration_library as npu_lib
from PytorchWildlife import utils as pw_utils
from PIL import Image
from domain.classify_detections import Classifier, txt_animalclasses
import numpy as np
import requests
import os
import logging
import datetime
import cv2

logger = logging.getLogger(__name__)

class AiModel():
    # Setting the device to use for computations ('cuda' indicates GPU, "npu" indicates intel NPU)
    #TODO: uncomment this: DEVICE = "npu" if npu_lib.backend.npu_available() else "cuda" if torch.cuda.is_available() else "cpu"
    DEVICE = "cpu"
    CLASSIFICATION_MODEL = os.path.join("C:/", "Users/", "stefa/", "Downloads","deepfaune-vit_large_patch14_dinov2.lvd142m.pt")

    def __init__(self):
        # Initializing the MegaDetectorV5 model for image detection
        logger.info("Initializing MegaDetectorV5 model for image detection to device {ImgDetector.DEVICE}...")
        self.detection_model = pw_detection.MegaDetectorV5(
            device=AiModel.DEVICE, pretrained=True)
        self.original_image = ""
        
        # Load classification model
        self.classifier = Classifier(AiModel.CLASSIFICATION_MODEL, AiModel.DEVICE)
        # Create required output folders
        os.makedirs("detection_output", exist_ok=True)
        os.makedirs("classification_output", exist_ok=True)

    def process_image(self, img_path):
        """Method to run detection model on provided image."""

        # Opening the image from local path, Converting the image to RGB format
        img = Image.open(img_path).convert("RGB")
        img_array = np.array(img)
        img_array.shape, img_array.dtype

        # Initializing the Yolo-specific transform for the image
        transform = pw_trans.MegaDetector_v5_Transform(target_size=self.detection_model.IMAGE_SIZE,
                                                       stride=self.detection_model.STRIDE)
        
        # Performing the detection on the single image
        results = self.detection_model.single_image_detection(transform(img_array), img_array.shape, img_path)
        #for key in results:
            #logging.debug(key, str(results[key]))

        # Saving the detection results 
        logger.info("Saving detection results...")
        pw_utils.save_detection_images(results, os.path.join(".","detection_output"), overwrite=False)

        return results

    def process_image_from_url(self, url, id):
        """Method to run detection model on image provided by URL"""

        logger.info("Processing image from url: "+url)
        # Opening the image from url
        img = Image.open(requests.get(url, stream=True).raw)
        # Save image to disk
        img_path = os.path.join("detection_output", "image_"+str(id)+"_"+
                                str(self.get_timestamp())+".jpg")
        img.save(img_path)
        logger.info("Saved processed image at: "+img_path)

        results = self.process_image(img_path)
        return [img_path, results]

    def classify(self, img_path, results):
        """Method to perform classification on detection result(s)."""

        logger.info("Running classification on %s image...", img_path)
        img = Image.open(img_path).convert("RGB")
        classification_id = 0
        classified_animals = []
        for xyxy in results["detections"].xyxy:
                # Cropping detection result(s) from original image leveraging detected boxes
                cropped_image = img.crop(xyxy)
                cropped_image_path = os.path.join("classification_output", str(classification_id)+'_cropped_image.jpg')
                cropped_image.save(cropped_image_path)
                logger.debug("Saved crop of image at %s.", cropped_image_path)
                # Performing classification
                classification_result = self.classify_crop(cropped_image)
                logger.info("Classification result: %s", classification_result)

                classified_animals.append({"id": classification_id,
                                        "classification": classification_result,
                                        "xyxy": xyxy})
                classification_id = classification_id+1

        img_path = self.build_classification_square(img, classified_animals)
        return img_path

    def build_classification_square(self, img, classified_animals):
        """Build square on classified animals."""

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
            text_len = len(str(animal["classification"]))
            # Draw black background rectangle to improve text readability
            classified_image = cv2.rectangle(classified_image, (x1, y1), (x2, y1 - 40), color, -1)
            animal["classification"][1] = round(animal["classification"][1], 2)
            # Add label to classification rectangle
            cv2.putText(classified_image, str(animal["classification"]), (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            cimg = Image.fromarray(classified_image)
            classified_image_path = os.path.join("classification_output",'classified_image.jpg')
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

    def get_timestamp(self):
        """Method to prepare timestamp string to apply to images naming"""

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return timestamp
    
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