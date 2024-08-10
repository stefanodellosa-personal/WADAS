from PytorchWildlife.models import detection as pw_detection
from PytorchWildlife.data import transforms as pw_trans
#import intel_npu_acceleration_library as npu_lib
from PytorchWildlife import utils as pw_utils
from PIL import Image
import numpy as np
import requests
import os
import logging
import datetime
import calendar
import time

logger = logging.getLogger(__name__)

class ImgDetector():
    # Setting the device to use for computations ('cuda' indicates GPU, "npu" indicates intel NPU)
    #TODO: uncomment this: DEVICE = "npu" if npu_lib.backend.npu_available() else "cuda" if torch.cuda.is_available() else "cpu"
    DEVICE = "cpu"

    def __init__(self):
        # Initializing the MegaDetectorV5 model for image detection
        logger.info("Initializing MegaDetectorV5 model for image detection to device {ImgDetector.DEVICE}...")
        self.detection_model = pw_detection.MegaDetectorV5(
            device=ImgDetector.DEVICE, pretrained=True)

    """Method to run detection model on provided image."""
    def process_image(self, img, id):
        # Save to disk
        os.makedirs("detection_output", exist_ok=True)
        img_path = os.path.join("detection_output", "image_"+str(id)+"_"+
                                str(self.get_timestamp())+".jpg")
        img.save(img_path)
        logger.info("Saved processed image at: "+img_path)

        img = np.array(img)
        img.shape, img.dtype

        # Initializing the Yolo-specific transform for the image
        transform = pw_trans.MegaDetector_v5_Transform(target_size=self.detection_model.IMAGE_SIZE,
                                                       stride=self.detection_model.STRIDE)
        
        # Performing the detection on the single image
        results = self.detection_model.single_image_detection(transform(img), img.shape, img_path)
        #for key in results:
            #logging.debug(key, str(results[key]))

        # Saving the detection results 
        logger.info("Saving detection results...")
        pw_utils.save_detection_images(results, os.path.join(".","detection_output"), overwrite=False)
        
        return img_path
    
    """Method to run detection model on provided image, from URL"""
    def process_image_from_url(self, url, id):
         # Opening the image from url, Converting the image to RGB format
        img = Image.open(requests.get(url, stream=True).raw).convert("RGB")
        logger.info("Processing image from url: "+url)
        img_path = self.process_image(img, id)
        
        return img_path

    """Method to prepare timestamp string to apply to images naming"""
    def get_timestamp(self):
        time_tuple = time.gmtime()
        timestamp = calendar.timegm(time_tuple)
        datetime.datetime.fromtimestamp(timestamp).strftime("%Y%m%d_%H%M%S")
        
        return timestamp