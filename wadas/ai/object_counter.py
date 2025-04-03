import os
from enum import Enum

import numpy as np
from ultralytics import solutions

from wadas.ai.ov_predictor import __model_folder__, load_ov_model


class TrackingRegion(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    def to_region(self, width: int, height: int) -> list[tuple[int, int]]:

        margin = 1 / 6  # 1/6 of the width or height
        if self == TrackingRegion.UP:
            region = [(0, height * margin), (width, height * margin)]
        elif self == TrackingRegion.DOWN:
            region = [(0, height * (1 - margin)), (width, height * (1 - margin))]
        elif self == TrackingRegion.LEFT:
            region = [(width * margin, 0), (width * margin, height)]
        elif self == TrackingRegion.RIGHT:
            region = [(width * (1 - margin), 0), (width * (1 - margin), height)]

        return [(int(dim[0]), int(dim[1])) for dim in region]


class ObjectCounter(solutions.ObjectCounter):

    def __init__(
        self,
        model: str,
        region: list[tuple[int, int]] | TrackingRegion,
        classes: list[int] = None,
        device: str = "auto",
        batch_size: int = 1,
        iou_threshold: float = 0.5,
        confidence_threshold: float = 0.3,
        **kwargs
    ):
        """
        Initializes the ObjectCounter class.
        Args:
            model (str): Path to the model file.
            region (list[tuple[int, int]] | TrackingRegion): List of tuples defining the
                                            region of interest. It is possible to define a line
                                            a polygon or an enum with predefined directions
            classes (list[int]): List of class indices to be counted.
            device (str, optional): Device to run the model on. Defaults to "auto".
            batch_size (int, optional): Number of images to process in a batch. Defaults to 1.
            **kwargs: Additional keyword arguments.
        """
        model = os.path.join(__model_folder__, model)
        super().__init__(
            model=model,
            region=None,
            classes=classes,
            batch_size=batch_size,
            iou=iou_threshold,
            conf=confidence_threshold,
            **kwargs
        )
        self.model.predictor.model.ov_compiled_model = load_ov_model(model, device)
        self.region = region

    def process_frames(self, frames: list[np.ndarray]) -> dict:
        """
        Processes a single frame.
        Args:
            frame (np.ndarray): Input frame.
        Returns:
            np.ndarray: Processed frame.
        """

        # If region is not initialized, set it to the first frame size
        if not self.region_initialized:
            if isinstance(self.region, TrackingRegion):
                self.region = self.region.to_region(frames[0].shape[1], frames[0].shape[0])

        for frame in frames:
            results = self.__call__(frame)

        # It will track the objects and count them at the end of the video
        # Result is in the form of a dictionary of classwise counts
        return results.classwise_count
