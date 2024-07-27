# Script to further identify MD animal detections using the DeepFaune classification model
# https://www.deepfaune.cnrs.fr/en/
# https://plmlab.math.cnrs.fr/deepfaune/software/-/tree/master
# Some code is created by the DeepFaune team and is indicated as so 

##############################################
############### MODEL SPECIFIC ###############
##############################################
# imports
import os
import sys
import numpy as np
import timm
import torch
from torch import tensor
import torch.nn as nn
from torchvision.transforms import InterpolationMode, transforms

# The following ClassifTools code snippet is created by the DeepFaune team.
# Orignal license is shown below.
# Source: https://plmlab.math.cnrs.fr/deepfaune/software/-/blob/master/classifTools.py
# The code is unaltered, except for two minor adjustments:
# 1. Accomodate for a non standard location of the model
# 2. Run on Apple Silicon GPU via MPS Metal GPU

################################################
############## CLASSIFTOOLS START ##############
################################################

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
# weight_path = "deepfaune-vit_large_patch14_dinov2.lvd142m.pt"
weight_path = os.path.join("D:/","Download","deepfaune-vit_large_patch14_dinov2.lvd142m.pt") # ADJUSTMENT 1
device = "cuda" if torch.cuda.is_available() else "cpu"

txt_animalclasses = {
    'fr': ["blaireau", "bouquetin", "cerf", "chamois", "chat", "chevre", "chevreuil", "chien", "ecureuil", "equide", "genette",
           "herisson", "lagomorphe", "loup", "lynx", "marmotte", "micromammifere", "mouflon",
           "mouton", "mustelide", "oiseau", "ours", "ragondin", "renard", "sanglier", "vache"],
    'en': ["badger", "ibex", "red deer", "chamois", "cat", "goat", "roe deer", "dog", "squirrel", "equid", "genet",
           "hedgehog", "lagomorph", "wolf", "lynx", "marmot", "micromammal", "mouflon",
           "sheep", "mustelid", "bird", "bear", "nutria", "fox", "wild boar", "cow"],
    'it': ["tasso", "stambecco", "cervo", "camoscio", "gatto", "capra", "capriolo", "cane", "scoiattolo", "equide", "genet",
           "riccio", "lagomorfo", "lupo", "lince", "marmotta", "micromammifero", "muflone",
           "pecora", "mustelide", "uccello", "orso", "nutria", "volpe", "cinghiale", "mucca"],
    'de': ["Dachs", "Steinbock", "Rothirsch", "Gämse", "Katze", "Ziege", "Rehwild", "Hund", "Eichhörnchen", "Equiden", "Ginsterkatze",
           "Igel", "Lagomorpha", "Wolf", "Luchs", "Murmeltier", "Kleinsäuger", "Mufflon",
           "Schaf", "Mustelide", "Vogen", "Bär", "Nutria", "Fuchs", "Wildschwein", "Kuh"],
    
}

class Classifier:
    def __init__(self):
        self.model = Model()
        self.model.loadWeights(weight_path)
        self.transforms = transforms.Compose([
            transforms.Resize(size=(CROP_SIZE, CROP_SIZE), interpolation=InterpolationMode.BICUBIC, max_size=None, antialias=None),
            transforms.ToTensor(),
            transforms.Normalize(mean=tensor([0.4850, 0.4560, 0.4060]), std=tensor([0.2290, 0.2240, 0.2250]))])

    def predictOnBatch(self, batchtensor, withsoftmax=True):
        return self.model.predict(batchtensor, withsoftmax)

    # croppedimage loaded by PIL
    def preprocessImage(self, croppedimage):
        preprocessimage = self.transforms(croppedimage)
        return preprocessimage.unsqueeze(dim=0)

class Model(nn.Module):
    def __init__(self):
        """
        Constructor of model classifier
        """
        super().__init__()
        self.base_model = timm.create_model(BACKBONE, pretrained=False, num_classes=len(txt_animalclasses['fr']),
                                            dynamic_img_size=True)
        print(f"Using {BACKBONE} with weights at {weight_path}, in resolution {CROP_SIZE}x{CROP_SIZE}")
        self.backbone = BACKBONE
        self.nbclasses = len(txt_animalclasses['fr'])

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
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # ADJUSTMENT 2
        self.to(device)
        total_output = []
        with torch.no_grad():
            x = data.to(device)
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
            params = torch.load(path, map_location=device)
            args = params['args']
            if self.nbclasses != args['num_classes']:
                raise Exception("You load a model ({}) that does not have the same number of class"
                                "({})".format(args['num_classes'], self.nbclasses))
            self.backbone = args['backbone']
            self.nbclasses = args['num_classes']
            self.load_state_dict(params['state_dict'])
        except Exception as e:
            print("\n/!\ Can't load checkpoint model /!\ because :\n\n " + str(e), file=sys.stderr)
            raise e

##############################################
############## CLASSIFTOOLS END ##############
##############################################

# This code snipped is created by EcoAssist team.
# Orignal license is shown below.
# Source: https://github.com/PetervanLunteren/EcoAssist/blob/main/classification_utils/model_types/deepfaune/classify_detections.py
# The code is unaltered, except for two minor adjustments:
# 1- function rename

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

# It constsist of code that is specific for this kind of model architechture, and 
# code that is generic for all model architectures that will be run via EcoAssist.
# Script created by Peter van Lunteren

# load model
classifier = Classifier()

# read label map
# not neccesary for yolov8 models to retreive label map exernally, as it is incorporated into the model itself

# predict from cropped image
# input: cropped PIL image
# output: unsorted classifications formatted as [['aardwolf', 2.3025326090220233e-09], ['african wild cat', 5.658252888451898e-08], ... ]
# no need to remove forbidden classes from the predictions, that will happen in infrence_lib.py
# this is also the place to preprocess the image if that need to happen

# def get_classification(PIL_crop):
# ADJUSTMENT 1

def get_classifications(PIL_crop):
    tensor_cropped = classifier.preprocessImage(PIL_crop)
    confs = classifier.predictOnBatch(tensor_cropped)[0,]
    lbls = txt_animalclasses['en']
    classifications = []
    for i in range(len(confs)):
        classifications.append([lbls[i], confs[i]])
    return classifications

##############################################
############### ECOASSIST END ################
##############################################

# Get single classification result (higher probability)
# input: cropped PIL image
# output: classification formatted as [['aardwolf', 2.3025326090220233e-09]
def get_classification(PIL_crop):
    classifications = get_classifications(PIL_crop)
    classified_animal = ['', 0]
    for result in classifications:
        if result[1] > classified_animal[1]:
            classified_animal = result
    return classified_animal