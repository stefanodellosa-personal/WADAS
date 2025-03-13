from wadas.domain.ai_model import AiModel
import argparse


import numpy as np
import cv2
from PIL import Image

import numpy as np
from scipy.spatial.distance import cdist


class KalmanFilter:
    """Kalman filter for smoothing detection coordinates or class probabilities"""

    def __init__(self, initial_value, process_variance=1, measurement_variance=10):
        self.x = np.array(initial_value, dtype=np.float32)  # State estimate
        self.P = np.eye(len(initial_value)) * 100.0  # Initial uncertainty
        self.Q = np.eye(len(initial_value)) * process_variance  # Process noise
        self.R = np.eye(len(initial_value)) * measurement_variance  # Measurement noise

    def update(self, measurement):
        """Kalman update step"""
        # Prediction (assume constant velocity)
        self.P += self.Q

        # Kalman Gain
        K = self.P @ np.linalg.inv(self.P + self.R)

        # Update state estimate
        self.x += K @ (np.array(measurement) - self.x)
        self.P = (np.eye(len(self.x)) - K) @ self.P

        return self.x


class ObjectTracker:
    """Tracks objects and smooths their class predictions over time"""

    def __init__(
        self, process_var=30, measurement_var=20, class_process_var=0.00, class_measurement_var=0.1
    ):
        self.trackers = {}  # ObjectID -> (KalmanFilter, KalmanClassSmoother)
        self.next_id = 0

        # Kalman filter settings
        self.process_var = process_var
        self.measurement_var = measurement_var
        self.class_process_var = class_process_var
        self.class_measurement_var = class_measurement_var

    def compute_centroid(self, xyxy):
        """Compute centroid of a bounding box"""
        return (xyxy[0] + xyxy[2]) / 2, (xyxy[1] + xyxy[3]) / 2

    def associate_detections(self, detections):
        """Match detections to existing trackers based on centroid distance"""
        if not self.trackers:
            return {i: self.next_id + i for i in range(len(detections))}  # Assign new IDs

        # Compute distance matrix
        track_ids = list(self.trackers.keys())
        track_positions = np.array([self.trackers[t][0].x for t in track_ids])
        detected_positions = np.array([self.compute_centroid(det["xyxy"]) for det in detections])

        distances = cdist(track_positions, detected_positions)
        assignment = np.argmin(distances, axis=0)

        # Assign IDs
        matches = {}
        for det_idx, track_idx in enumerate(assignment):
            if distances[track_idx, det_idx] < 50:  # Threshold for same object
                matches[det_idx] = track_ids[track_idx]
            else:
                matches[det_idx] = self.next_id
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

            if obj_id not in self.trackers:
                self.trackers[obj_id] = (
                    KalmanFilter(
                        [x, y], self.process_var, self.measurement_var
                    ),  # Position tracker
                    {
                        cls: KalmanFilter([p], self.class_process_var, self.class_measurement_var)
                        for cls, p in class_probs.items()
                    },  # Class smoothers
                )

            # Update position
            position_filter = self.trackers[obj_id][0]
            smoothed_pos = position_filter.update([x, y])

            # Convert smoothed_pos to xyxy
            h, w = xyxy[3] - xyxy[1], xyxy[2] - xyxy[0]
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

        self.trackers = {
            k["id"]: self.trackers[k["id"]] for k in updated_tracks
        }  # Remove lost tracks
        return updated_tracks


def draw_bbox(frame, animal, color=(0, 0, 255)):
    """Draw bounding box on frame"""
    x1, y1, x2, y2 = animal["xyxy"]
    label = f"[{animal['id']}] {animal['classification'][0]}: {animal['classification'][1]:.2f}"
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


def main(video):

    ai_pipeline = AiModel()
    ai_pipeline.classification_threshold = 0.0
    ai_pipeline.detection_threshold = 0.0
    # ai_pipeline.video_fps = 5

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
