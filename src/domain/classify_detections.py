# Script to further identify MD animal detections using the DeepFaune classification model
# https://www.deepfaune.cnrs.fr/en/
# https://plmlab.math.cnrs.fr/deepfaune/software/-/tree/master
# Some code is created by the DeepFaune team and is indicated as so

# ##############################################
# ############### MODEL SPECIFIC ###############
# ##############################################
import sys

import numpy as np
import timm
import torch
import torch.nn as nn
from torch import tensor
from torchvision.transforms import InterpolationMode, transforms

from ai.openvino_model import OVClassificationModel

# The following ClassifTools code snippet is created by the DeepFaune team.
# Orignal license is shown below.
# Source: https://plmlab.math.cnrs.fr/deepfaune/software/-/blob/master/classifTools.py
# The code is unaltered, except for two minor adjustments:
# 1. Accomodate for a non standard location of the model
# 2. Run parametric device

# ################################################
# ############## CLASSIFTOOLS START ##############
# ################################################

# Copyright CNRS 2023

# simon.chamaille@cefe.cnrs.fr; vincent.miele@univ-lyon1.fr

# This software is a computer program whose purpose is to identify
# animal species in camera trap images.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

CROP_SIZE = 182
BACKBONE = "vit_large_patch14_dinov2.lvd142m"
# weight_path = "deepfaune-vit_large_patch14_dinov2.lvd142m.pt" # ADJUSTMENT 1

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


class Classifier:
    def __init__(self, weight_path, device):  # ADJUSTMENT 1, 2
        self.model = OVClassificationModel(weight_path, device)
        self.model.loadWeights(weight_path)
        self.transforms = transforms.Compose(
            [
                transforms.Resize(
                    size=(CROP_SIZE, CROP_SIZE),
                    interpolation=InterpolationMode.BICUBIC,
                    max_size=None,
                    antialias=None,
                ),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=tensor([0.4850, 0.4560, 0.4060]),
                    std=tensor([0.2290, 0.2240, 0.2250]),
                ),
            ]
        )

    def predictOnBatch(self, batchtensor, withsoftmax=True):
        return self.model.predict(batchtensor, withsoftmax)

    # croppedimage loaded by PIL
    def preprocessImage(self, croppedimage):
        preprocessimage = self.transforms(croppedimage)
        return preprocessimage.unsqueeze(dim=0)


class Model(nn.Module):
    def __init__(self, weight_path, device):  # ADJUSTMENT 1, 2
        """
        Constructor of model classifier
        """
        super().__init__()
        self.base_model = timm.create_model(
            BACKBONE,
            pretrained=False,
            num_classes=len(txt_animalclasses["fr"]),
            dynamic_img_size=True,
        )
        print(
            f"Using {BACKBONE} with weights at {weight_path}, in resolution {CROP_SIZE}x{CROP_SIZE}"
        )
        self.backbone = BACKBONE
        self.nbclasses = len(txt_animalclasses["fr"])
        self.device = device

    def forward(self, input):
        x = self.base_model(input)
        return x

    def predict(self, data, withsoftmax=True):
        """
        Predict on test DataLoader
        :param test_loader: test dataloader: torch.utils.data.DataLoader
        :return: numpy array of predictions without soft max
        """
        self.eval()
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # ADJUSTMENT 1
        self.to(self.device)  # ADJUSTMENT 2
        total_output = []
        with torch.no_grad():
            x = data.to(self.device)  # ADJUSTMENT 2
            if withsoftmax:
                output = self.forward(x).softmax(dim=1)
            else:
                output = self.forward(x)
            total_output += output.tolist()

        return np.array(total_output)

    def loadWeights(self, path):
        """
        :param path: path of .pt save of model
        """
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # ADJUSTMENT 2

        if path[-3:] != ".pt":
            path += ".pt"
        try:
            params = torch.load(path, map_location=self.device)  # ADJUSTMENT
            args = params["args"]
            if self.nbclasses != args["num_classes"]:
                raise Exception(
                    "You load a model ({}) that does not have the same number of class"
                    "({})".format(args["num_classes"], self.nbclasses)
                )
            self.backbone = args["backbone"]
            self.nbclasses = args["num_classes"]
            self.load_state_dict(params["state_dict"])
        except Exception as e:
            print(
                "\n! Can't load checkpoint model! reason :\n\n " + str(e),
                file=sys.stderr,
            )
            raise e


# ##############################################
# ############## CLASSIFTOOLS END ##############
# ##############################################
