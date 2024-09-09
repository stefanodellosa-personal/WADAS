import time
import cv2
from cv2_enumerate_cameras import enumerate_cameras

TRESHOLD = int(180)
MINIMUM_CONTOUR_AREA = int(500)
MS_SUBSAMPLE_RATE = int(1000)
MAX_DETECTION_PER_S = int(1)

def main():
    """Main function."""

    for camera_info in enumerate_cameras(cv2.CAP_MSMF):
        print(f'{camera_info.index}: {camera_info.name}')

    camera_info = enumerate_cameras(cv2.CAP_MSMF)[0]
    process_video_Capture(camera_info.index, camera_info.backend)

def process_video_Capture(index, backend):
    cap = cv2.VideoCapture(index, backend)

   # Create Background Subtractor MOG2 object
    backSub = cv2.createBackgroundSubtractorMOG2()

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream.")
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    print('Length: %.2f | Width: %.2f | Height: %.2f | Fps: %.2f' % (length, width, height, fps))

    last_detection_time = 0

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        cap.set(cv2.CAP_PROP_POS_MSEC, MS_SUBSAMPLE_RATE)

        if ret:
            # Apply background subtraction
            foreground_mask = backSub.apply(frame)

            # apply global threshold to remove shadows
            retval, mask_thresh = cv2.threshold(foreground_mask, TRESHOLD, 255, cv2.THRESH_BINARY)

            # set the kernal
          #  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            # Apply erosion
           # mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)

            # Find contours
            contours, hierarchy = cv2.findContours(mask_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # filtering contours using list comprehension
            approved_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > MINIMUM_CONTOUR_AREA]
            frame_out = frame.copy()
            if len(approved_contours) > 0:
                # Limit the amount of frame processed per second
                current_detection_time = time.time()
                if (current_detection_time - last_detection_time) < MAX_DETECTION_PER_S:
                    continue

                print("DETECTION!")
                last_detection_time = current_detection_time
                for cnt in approved_contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    frame_out = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 200), 3)

                # Display the resulting frame
                cv2.imshow("Frame_final", frame_out)

            # Press Q on keyboard to exit
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        else:
            break

    # When everything done, release the video capture and writer object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
