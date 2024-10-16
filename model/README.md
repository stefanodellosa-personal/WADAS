# Generate the models

To generate the detection and classification models, use the next steps:

1. Download the deepfaune model from this [URL](https://pbil.univ-lyon1.fr/software/download/deepfaune/v1.1/deepfaune-vit_large_patch14_dinov2.lvd142m.pt)
2. Run the `export_models.py` script. It should generate the following models: `detection_model.onnx`, `classification_model.xml` and `classification_model.xml`
3. Copy those models to the repo root folder
