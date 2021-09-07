#!/usr/bin/env python
import cv2
from time import time
import numpy as np
from PIL import Image

FRAMERATE = 1  # 1 FPS
CAPTURE_BUFFER = 5  # Number of frames to capture before/after motion


def detect_motion(i0, i1):

    # res = cv2.absdiff(i0, i1)
    # res = res.astype(np.uint8)
    # return np.count_nonzero(res) / res.size


def main():
    cap = cv2.VideoCapture(0)

    # Save the last
    previous_images = []

    # Time last image was saved
    t0 = time()

    while True:

        # Capture frame
        ret, frame = cap.read()

        # Display frame
        cv2.imshow('frame', frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # If framerate has been met for current frame, process
        if time() - t0 >= 1 / FRAMERATE:
            # Save new image to previous_images
            if len(previous_images) >= 5:
                previous_images.pop(0)
            previous_images.append(frame)

            # Update time last image was saved
            t0 = time()

            # Check for difference in last 2 images
            if len(previous_images) > 1:
                print(detect_motion(previous_images[-2], previous_images[-1]))

    # Exit
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
