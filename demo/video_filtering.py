from wadas.domain.ai_model import AiModel
import argparse


import numpy as np
import cv2
from PIL import Image

import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


class KalmanFilter:
    """Kalman filter for smoothing detection coordinates or class probabilities"""

    def __init__(self, initial_value, process_variance=1, measurement_variance=10, extra=None):
        self.x = np.array(initial_value, dtype=np.float32)  # State estimate [x, y, vx, vy]
        self.dim = len(initial_value) // 2  # Dimension of state
        self.P = np.eye(len(initial_value)) * 100.0  # Initial uncertainty
        self.Q = np.eye(len(initial_value)) * process_variance  # Process noise
        self.R = np.eye(len(initial_value[: self.dim])) * measurement_variance  # Measurement noise
        self.extra = extra

    def update(self, measurement):
        """Kalman update step"""
        # Prediction
        self.x[: self.dim] += self.x[self.dim :]  # Update position with velocity
        self.P += self.Q

        # Kalman Gain
        K = self.P[: self.dim, : self.dim] @ np.linalg.inv(self.P[: self.dim, : self.dim] + self.R)

        # Update state estimate
        self.x[: self.dim] += K @ (np.array(measurement) - self.x[: self.dim])
        self.P[: self.dim, : self.dim] = (np.eye(self.dim) - K) @ self.P[: self.dim, : self.dim]

        return self.x


def compute_iou(box1, box2):
    """Compute Intersection over Union (IoU) between two bounding boxes"""
    x1, y1, x2, y2 = box1
    x1_p, y1_p, x2_p, y2_p = box2

    xi1, yi1 = max(x1, x1_p), max(y1, y1_p)
    xi2, yi2 = min(x2, x2_p), min(y2, y2_p)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_p - x1_p) * (y2_p - y1_p)
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area


class ObjectTracker:
    """Tracks objects and smooths their class predictions over time"""

    def __init__(
        self,
        process_var=30,
        measurement_var=1,
        class_process_var=0.00,
        class_measurement_var=0.1,
        max_missed=5,
    ):
        self.trackers = {}  # ObjectID -> (KalmanFilter, KalmanClassSmoother, missed_count)
        self.next_id = 0

        # Kalman filter settings
        self.process_var = process_var
        self.measurement_var = measurement_var
        self.class_process_var = class_process_var
        self.class_measurement_var = class_measurement_var
        self.max_missed = max_missed

    def compute_centroid(self, xyxy):
        """Compute centroid of a bounding box"""
        return (xyxy[0] + xyxy[2]) / 2, (xyxy[1] + xyxy[3]) / 2

    def associate_detections(self, detections):
        """Match detections to existing trackers based on IoU and Hungarian algorithm"""
        if not self.trackers:
            return {i: self.next_id + i for i in range(len(detections))}  # Assign new IDs

        # Compute IoU matrix
        track_ids = list(self.trackers.keys())
        track_boxes = []
        for t in track_ids:
            h, w = self.trackers[t][0].extra["h"], self.trackers[t][0].extra["w"]
            x, y, _, __ = self.trackers[t][0].x
            xyxy = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]
            track_boxes.append(xyxy)
        detected_boxes = [det["xyxy"] for det in detections]

        iou_matrix = np.zeros((len(track_boxes), len(detected_boxes)))
        for i, track_box in enumerate(track_boxes):
            for j, detected_box in enumerate(detected_boxes):
                iou_matrix[i, j] = compute_iou(track_box, detected_box)

        # Hungarian algorithm for optimal assignment
        row_ind, col_ind = linear_sum_assignment(-iou_matrix)

        # Assign IDs
        matches = {}
        for r, c in zip(row_ind, col_ind):
            if iou_matrix[r, c] > 0.3:  # Threshold for same object
                matches[c] = track_ids[r]
            else:
                matches[c] = self.next_id
                self.next_id += 1

        for j in range(len(detected_boxes)):
            if j not in col_ind:
                matches[j] = self.next_id
                self.next_id += 1

        return matches

    def update(self, detections):
        """Update all object trackers with new detections"""

        # Compute the detections
        matches = self.associate_detections(detections)

        updated_tracks = []
        for det_idx, obj_id in matches.items():
            xyxy = detections[det_idx]["xyxy"]
            class_probs = detections[det_idx]["class_probs"]

            # Compute centroid
            x, y = self.compute_centroid(xyxy)
            h, w = xyxy[3] - xyxy[1], xyxy[2] - xyxy[0]

            if obj_id not in self.trackers:
                self.trackers[obj_id] = (
                    KalmanFilter(
                        [x, y, 0, 0], self.process_var, self.measurement_var, extra={"h": h, "w": w}
                    ),  # Position tracker with speed
                    {
                        cls: KalmanFilter(
                            [p, 0], self.class_process_var, self.class_measurement_var
                        )
                        for cls, p in class_probs.items()
                    },  # Class smoothers
                    0,  # Missed count
                )
            else:
                self.trackers[obj_id][0].extra = {"h": h, "w": w}
                self.trackers[obj_id] = (
                    self.trackers[obj_id][0],
                    self.trackers[obj_id][1],
                    0,
                )  # Reset missed count

            # Update position
            position_filter = self.trackers[obj_id][0]
            smoothed_pos = position_filter.update([x, y])

            # Convert smoothed_pos to xyxy
            smoothed_pos = [
                smoothed_pos[0] - w / 2,
                smoothed_pos[1] - h / 2,
                smoothed_pos[0] + w / 2,
                smoothed_pos[1] + h / 2,
            ]

            # Convert to int
            smoothed_pos = [int(p) for p in smoothed_pos]

            # Update classification
            class_filters = self.trackers[obj_id][1]
            smoothed_probs = {
                cls: class_filters[cls].update([p])[0] for cls, p in class_probs.items()
            }

            # Build classification result
            logits = np.array(list(smoothed_probs.values()))
            labels = list(smoothed_probs.keys())
            classification_result = labels[np.argmax(logits)], max(logits)

            updated_tracks.append(
                {"id": obj_id, "classification": classification_result, "xyxy": smoothed_pos}
            )

        # Increment missed count for unmatched trackers
        for obj_id in self.trackers.keys():
            if obj_id not in [track["id"] for track in updated_tracks]:
                self.trackers[obj_id] = (
                    self.trackers[obj_id][0],
                    self.trackers[obj_id][1],
                    self.trackers[obj_id][2] + 1,
                )
                if self.trackers[obj_id][2] <= self.max_missed:
                    # Process unmatched tracked objects
                    position_filter = self.trackers[obj_id][0]
                    smoothed_pos = position_filter.update(position_filter.x[:2])

                    # Convert smoothed_pos to xyxy
                    h, w = position_filter.extra["h"], position_filter.extra["w"]
                    smoothed_pos = [
                        smoothed_pos[0] - w / 2,
                        smoothed_pos[1] - h / 2,
                        smoothed_pos[0] + w / 2,
                        smoothed_pos[1] + h / 2,
                    ]

                    # Convert to int
                    smoothed_pos = [int(p) for p in smoothed_pos]

                    # Update classification
                    class_filters = self.trackers[obj_id][1]
                    smoothed_probs = {
                        cls: class_filters[cls].update([class_filters[cls].x[0]])[0]
                        for cls in class_filters.keys()
                    }

                    # Build classification result
                    logits = np.array(list(smoothed_probs.values()))
                    labels = list(smoothed_probs.keys())
                    classification_result = labels[np.argmax(logits)], max(logits)

                    updated_tracks.append(
                        {
                            "id": obj_id,
                            "classification": classification_result,
                            "xyxy": smoothed_pos,
                        }
                    )

        # Remove lost tracks
        self.trackers = {
            k["id"]: self.trackers[k["id"]]
            for k in updated_tracks
            if self.trackers[k["id"]][2] <= self.max_missed
        }

        return updated_tracks


def draw_bbox(frame, animal, color=(0, 0, 255)):
    """Draw bounding box on frame"""
    x1, y1, x2, y2 = animal["xyxy"]
    # label = f"[{animal['id']}] {animal['classification'][0]}: {animal['classification'][1]:.2f}"
    label = animal["classification"][0]
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


def main(video):

    ai_pipeline = AiModel()
    ai_pipeline.classification_threshold = 0.0
    ai_pipeline.detection_threshold = 0.0
    ai_pipeline.video_fps = 4

    tracker = ObjectTracker()
    idx = 0
    for result, _detected_image_path, frame_path in ai_pipeline.process_video(video, True):
        frame = np.array(Image.open(frame_path).convert("RGB"))
        frame_copy = frame.copy()

        _, classified_animals = ai_pipeline.classify(frame_path, result)

        if classified_animals:
            for animal in classified_animals:
                draw_bbox(frame, animal)

        tracked_animal = tracker.update(classified_animals)

        if classified_animals:
            for animal in tracked_animal:
                draw_bbox(frame_copy, animal)

        cv2.imshow("Detection & Classification", frame)
        cv2.imshow("Detection & Classification with Tracking", frame_copy)
        if idx == 0:
            cv2.waitKey(0)
        idx += 1

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=str)
    args = parser.parse_args()
    main(args.video)
