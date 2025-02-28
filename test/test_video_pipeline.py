# This file is part of WADAS project.
#
# WADAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WADAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WADAS. If not, see <https://www.gnu.org/licenses/>.
#
# Author(s): Stefano Dell'Osa, Alessandro Palla, Cesare Di Mauro, Antonio Farina
# Date: 2024-08-14
# Description: Test for AI video pipeline

import os

import numpy as np
import pytest

from wadas.domain.ai_model import AiModel


@pytest.fixture
def init():
    AiModel.classification_threshold = 0.5
    AiModel.detection_threshold = 0.5
    AiModel.language = "en"
    AiModel.detection_device = "auto"
    AiModel.classification_device = "auto"


def test_video_detection_and_classification(init):
    ai_pipeline = AiModel()

    assert ai_pipeline.classification_threshold == 0.5
    assert ai_pipeline.detection_threshold == 0.5
    assert ai_pipeline.language == "en"
    assert ai_pipeline.classification_device == "auto"
    assert ai_pipeline.detection_device == "auto"
    assert ai_pipeline.check_model()

    # This one is the video of a bear
    VIDEO_URL = "https://videos.pexels.com/video-files/857097/857097-hd_1280_720_30fps.mp4"
    for result, frame in ai_pipeline.process_video(VIDEO_URL, True):
        assert result is not None
        assert result["detections"].xyxy.shape == (1, 4)
        assert result["detections"].xyxy.dtype == np.float32

        assert result["detections"].mask is None
        assert result["detections"].confidence.shape == (1,)
        assert result["detections"].confidence.dtype == np.float32

        img_path, classified_animals = ai_pipeline.classify(frame, result)

        assert classified_animals is not None
        if len(classified_animals) > 0:
            assert classified_animals[0]["id"] == 0
            assert classified_animals[0]["classification"][0] == "bear"
            assert classified_animals[0]["classification"][1] > 0.7

            assert os.path.exists(img_path)
            assert classified_animals[0]["xyxy"].dtype == np.float32


def test_video_detection_and_classification_empty(init):
    ai_pipeline = AiModel()

    assert ai_pipeline.classification_threshold == 0.5
    assert ai_pipeline.detection_threshold == 0.5
    assert ai_pipeline.language == "en"
    assert ai_pipeline.classification_device == "auto"
    assert ai_pipeline.detection_device == "auto"
    assert ai_pipeline.check_model()
    # This one is the video of a waterfall => No animals
    VIDEO_URL = "https://videos.pexels.com/video-files/6981411/6981411-hd_1920_1080_25fps.mp4"
    animals = []
    for result, frame in ai_pipeline.process_video(VIDEO_URL, True):
        _, classified_animals = ai_pipeline.classify(frame, result)
        if classified_animals:
            animals.append(classified_animals)

    assert len(animals) == 0
