from PytorchWildlife.models import detection as pw_detection
import openvino.properties as props
import openvino as ov
import numpy as np
import torch

core = ov.Core()
core.set_property({props.cache_dir: "cache"})
#TODO: Ann NPU specific properties

class DetectionModel():
    def __init__(self, device="cpu") -> None:
        print("Loading Openvino model")
        
        ov_model = core.read_model("detection_model.onnx")
        self.model = ov.compile_model(ov_model, device_name=device.upper())

    def __call__(self, img: torch.tensor):
       results = [torch.tensor(t) for t in self.model(img).values()]
       return results


class OVMegaDetectorV5(pw_detection.MegaDetectorV5):
    def __init__(self, device="cpu"):
        self.model = DetectionModel(device)
        self.device = "cpu"  # torch device, keep to CPU when using with OpenVINO


class OVClassificationModel():
    def __init__(self, weight_path, device):

        ov_model = core.read_model("classification_model.xml")
        self.model = ov.compile_model(ov_model, device_name=device.upper())
        self.device = "cpu"

    def forward(self, input):
        results = [torch.tensor(t) for t in self.model(input).values()]
        if len(results) == 1:
            return results[0]
        return results

    def predict(self, data, withsoftmax=True):
        """
        Predict on test DataLoader
        :param test_loader: test dataloader: torch.utils.data.DataLoader
        :return: numpy array of predictions without soft max
        """
        total_output = []
        with torch.no_grad():
            x = data.to(self.device) # ADJUSTMENT 2
            if withsoftmax:
                output = self.forward(x).softmax(dim=1)
            else:
                output = self.forward(x)
            total_output += output.tolist()

        return np.array(total_output)

    def loadWeights(self, path):
        pass