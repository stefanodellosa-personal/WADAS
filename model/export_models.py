import os
import subprocess

import numpy as np
import openvino as ov
import requests
import timm
import torch
from PIL import Image
from PytorchWildlife.data import transforms as pw_trans
from PytorchWildlife.models import detection as pw_detection
from torchvision.transforms import InterpolationMode, transforms
from tqdm import tqdm

CROP_SIZE = 182
WEIGHT_PATH = "deepfaune-vit_large_patch14_dinov2.lvd142m.pt"
# Line too long
URL = (
    "https://www.provincia.bz.it/agricoltura-foreste/"
    "fauna-caccia-pesca/images/braunbaer_6016_L.jpg"
)


class Model(torch.nn.Module):
    def __init__(self, weight_path, device="cpu", version="v1.1"):
        """
        Constructor of model classifier
        """
        super().__init__()

        if not os.path.exists(weight_path):
            self.download_weights(weight_path, version)

        params = torch.load(weight_path, map_location=device, weights_only=False)
        self.base_model = timm.create_model(
            params["args"]["backbone"],
            pretrained=False,
            num_classes=params["args"]["num_classes"],
            dynamic_img_size=True,
        )
        self.load_state_dict(params["state_dict"])

    def forward(self, input):
        return self.base_model(input)

    def download_weights(self, fname, version):
        url = f"https://pbil.univ-lyon1.fr/software/download/deepfaune/{version}/{fname}"
        print(f"Downloading weights from {url}")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        chunk_size = 8192

        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(fname, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            raise RuntimeError("Could not download file")


def main():

    detection_model = pw_detection.MegaDetectorV5(device="cpu", pretrained=True)

    img = Image.open(requests.get(URL, stream=True).raw).convert("RGB")
    img_array = np.array(img)

    transform = pw_trans.MegaDetector_v5_Transform(
        target_size=detection_model.IMAGE_SIZE, stride=detection_model.STRIDE
    )

    transformed_img = transform(img_array).unsqueeze(0)

    print("Exporting detection model to OpenVINO...")
    # Need to export via ONNX as OV returns error in torch scripting
    torch.onnx.export(detection_model.model, transformed_img, "detection_model.onnx")
    subprocess.run("ovc detection_model.onnx --compress_to_fp16 True", shell=True)
    os.remove("detection_model.onnx")

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
        print("Exporting classification model to OpenVINO...")

        ov_model = ov.convert_model(classification_model, example_input=tensor_cropped)
        ov.save_model(ov_model, "classification_model.xml")
        # torch.onnx.export(classification_model, tensor_cropped, "classification_model.onnx")


if __name__ == "__main__":
    main()
