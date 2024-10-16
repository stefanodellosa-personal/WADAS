import openvino.properties as props
import openvino as ov
import torch
import os

core = ov.Core()
core.set_property({props.cache_dir: "cache"})


class OVModel:
    def __init__(self, model_name, device):
        """Base class for OpenVino models"""
        self.device = device
        self.model_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", "model"
        )
        self.model = self.compile_model(self.load_model(model_name))

    def load_model(self, model_name):
        """Load model from file"""
        return core.read_model(os.path.join(self.model_folder, model_name))

    def get_available_device(self):
        """Get available devices"""
        return core.available_devices

    def compile_model(self, model):
        """Compile model"""
        return ov.compile_model(
            model,
            device_name=self.device.upper(),
        )

    def __call__(self, input: torch.Tensor) -> torch.Tensor | list[torch.Tensor]:
        """Run model"""
        results = [torch.tensor(t) for t in self.model(input).values()]
        if len(results) == 1:
            return results[0]
        return results
