import sys
import os

import numpy as np
import openvino as ov
from PIL import Image
from PytorchWildlife.data import transforms as pw_trans
from PytorchWildlife.models import detection as pw_detection
import requests
import torch
from torchvision.transforms import InterpolationMode, transforms

from domain.classify_detections import Model

CROP_SIZE = 182
BACKBONE = "vit_large_patch14_dinov2.lvd142m"
# Line too long
URL = (
    "https://www.provincia.bz.it/agricoltura-foreste/"
    "fauna-caccia-pesca/images/braunbaer_6016_L.jpg"
)
WEIGHT_PATH = f"{os.path.join('../', 'deepfaune-vit_large_patch14_dinov2.lvd142m.pt')}"

_thisdir = os.path.dirname(os.path.abspath(__file__))
print(_thisdir)
sys.path.append(os.path.join(_thisdir, "../src"))


def main():

    detection_model = pw_detection.MegaDetectorV5(device="cpu", pretrained=True)

    img = Image.open(requests.get(URL, stream=True).raw).convert("RGB")
    img_array = np.array(img)

    transform = pw_trans.MegaDetector_v5_Transform(
        target_size=detection_model.IMAGE_SIZE, stride=detection_model.STRIDE
    )

    transformed_img = transform(img_array).unsqueeze(0)

    print(transformed_img.shape, transformed_img.dtype, type(transformed_img))

    print("Exporting detection model to OpenVINO...")
    torch.onnx.export(detection_model.model, transformed_img, "detection_model.onnx")

    results = detection_model.single_image_detection(
        transform(img_array), img_array.shape, "tmp.png", 0.5
    )

    for xyxy in results["detections"].xyxy:
        cropped_image = img.crop(xyxy)

        crop_transform = transforms.Compose(
            [
                transforms.Resize(
                    size=(CROP_SIZE, CROP_SIZE),
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

        tensor_cropped = crop_transform(cropped_image).unsqueeze(dim=0)

        classification_model = Model(WEIGHT_PATH, "cpu")
        classification_model.loadWeights(WEIGHT_PATH)
        print("Exporting classification model to OpenVINO...")

        ov_model = ov.convert_model(classification_model, example_input=tensor_cropped)
        ov.save_model(ov_model, "classification_model.xml")
        # torch.onnx.export(classification_model, tensor_cropped, "classification_model.onnx")


main()
