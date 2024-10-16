from ai.models import OVMegaDetectorV5, Classifier
from ai.pipeline import DetectionPipeline
from PIL import Image
import requests
import numpy as np
import pytest

TEST_URL = "https://www.parks.it/tmpFoto/30079_4_PNALM.jpeg"


def test_detection_model():
    """Test if model exists."""
    assert OVMegaDetectorV5.check_model()


def test_classification_model():
    assert Classifier.check_model()


@pytest.fixture
def detection_pipeline():
    pipeline = DetectionPipeline(device="cpu")
    assert pipeline.check_models()
    return pipeline


def test_detection(detection_pipeline):
    """Test detection pipeline."""

    img = Image.open(requests.get(TEST_URL, stream=True).raw).convert("RGB")
    results = detection_pipeline.run_detection(img, 0.5)

    assert results is not None
    assert "detections" in results

    assert len(results["detections"].xyxy) == 1

    # Test with a valid image
    assert results["detections"].xyxy.shape == (1, 4)
    assert results["detections"].xyxy.dtype == np.float32
    assert results["detections"].xyxy.flatten().tolist() == [289, 175, 645, 424]

    assert results["detections"].mask == None
    assert results["detections"].confidence.item() > 0.94
    assert results["detections"].confidence.shape == (1,)
    assert results["detections"].confidence.dtype == np.float32

    assert results["labels"] == ["animal 0.94"]


def test_classification(detection_pipeline):

    img = Image.open(requests.get(TEST_URL, stream=True).raw).convert("RGB")
    results = detection_pipeline.run_detection(img, 0.5)

    classified_animals = detection_pipeline.classify(img, results, 0.5)

    print(classified_animals)

    assert classified_animals is not None

    assert len(classified_animals) == 1

    assert classified_animals[0]["id"] == 0

    assert classified_animals[0]["classification"][0] == "bear"
    assert classified_animals[0]["classification"][1].item() > 0.96

    assert classified_animals[0]["xyxy"].flatten().tolist() == [289, 175, 645, 424]
    assert classified_animals[0]["xyxy"].dtype == np.float32
