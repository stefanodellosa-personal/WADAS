from PytorchWildlife.models import detection as pw_detection
from PytorchWildlife.data import transforms as pw_trans
#import intel_npu_acceleration_library as npu_lib
from PytorchWildlife import utils as pw_utils
from PIL import Image
import domain.classify_detections
import numpy as np
import requests
import os
import logging
import datetime
import calendar
import time
import cv2

logger = logging.getLogger(__name__)

class AiModel():
    # Setting the device to use for computations ('cuda' indicates GPU, "npu" indicates intel NPU)
    #TODO: uncomment this: DEVICE = "npu" if npu_lib.backend.npu_available() else "cuda" if torch.cuda.is_available() else "cpu"
    DEVICE = "cpu"

    def __init__(self):
        # Initializing the MegaDetectorV5 model for image detection
        logger.info("Initializing MegaDetectorV5 model for image detection to device {ImgDetector.DEVICE}...")
        self.detection_model = pw_detection.MegaDetectorV5(
            device=AiModel.DEVICE, pretrained=True)
        self.original_image = ""
        
        os.makedirs("detection_output", exist_ok=True)

    def process_image(self, img, id):
        """Method to run detection model on provided image."""

        # Save image to disk
        img_path = os.path.join("detection_output", "image_"+str(id)+"_"+
                                str(self.get_timestamp())+".jpg")
        img.save(img_path)
        logger.info("Saved processed image at: "+img_path)

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
        
        return img_path
    

    def process_image_from_url(self, url, id):
        """Method to run detection model on provided image, from URL"""

         # Opening the image from url, Converting the image to RGB format
        img = Image.open(requests.get(url, stream=True).raw).convert("RGB")

        logger.info("Processing image from url: "+url)
        img_path = self.process_image(img, id)
        
        return img_path

    def classify(self, img, results):
        """Method to perform classification on detection result(s)."""

        classification_id = 0
        classified_animals = []
        for xyxy in results["detections"].xyxy:
                # Cropping detection result(s) from original image leveraging detected boxes
                cropped_image = img.crop(xyxy)
                cropped_image.save(os.path.join("demo_output", str(classification_id)+'_cropped_image.jpg'))
                
                # Performing classification
                classification_result = classify_detections.get_classification(cropped_image)
                #print(classification_result)
                classified_animals.append({"id": classification_id,
                                        "classification": classification_result,
                                        "xyxy": xyxy})
                classification_id = classification_id+1

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
            cimg.save(os.path.join("demo_output",'classified_image.jpg'))
        #display(cimg)

    def get_timestamp(self):
        """Method to prepare timestamp string to apply to images naming"""

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return timestamp