#!/usr/bin/env python
import cv2
from time import time
import os
import datetime
import numpy as np
import atexit


def exit_handler():
    os.system('rm -rf ' + TMP_DIR)


def currentTime():
    # Returns [year, month, day, hour, minute, second]
    return datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S').split(':')


def mkdir(directory, verbose=False):
    try:
        os.makedirs(directory)
    except:
        if verbose:
            print('File exsists: {}'.format(directory))


def compareImages(image0, image1, difference=0.3):
    # Returns True or False depending on if the images are more than difference apart from each other
    # difference is a 0.0 to 1.0
    MAX_ERROR = 195075.0  # This is the error between a white and black image

    # print(image0, image1, end=' ')

	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images
	# NOTE: the two images must have the same dimension
    err = np.sum((image0.astype("float") - image1.astype("float")) ** 2)
    err /= float(image0.shape[0] * image0.shape[1])

    print(str(round(100*err/MAX_ERROR, 3)) + '%')

    return(err / MAX_ERROR >= difference)


if __name__ == '__main__':
    # Image save directories
    TMP_DIR = '/tmp/camera'
    PERM_DIR = 'savedImages4'

    # How different images have to be to "detect" motion
    DIFFERENCE_PERCENTAGE = 0.01

    # Remove TMP_DIR on exit
    atexit.register(exit_handler)

    # How many images to save after motion is detected
    imagesSavedAfterMotion = 10
    # Counter for imagesSavedAfterMotion
    saveImageCounter = 0

    # Capture device
    cap = cv2.VideoCapture(0)

    # Create image save directories
    mkdir(TMP_DIR)
    mkdir(PERM_DIR)

    # Images to compare to check for motion
    currentImages = []

    # Running loop
    while True:
        # Initial time of loop
        t0 = time()

        # Capture image
        ret, frame = cap.read()

        # Write to file
        year, month, day, hour, minute, second = currentTime()
        filename = '{}-{}-{}-{}-{}-{}'.format(year, month, day, hour, minute, second)
        if saveImageCounter > 0:
            cv2.imwrite('{}/{}.jpg'.format(PERM_DIR, filename), frame)
            saveImageCounter -= 1
        else:
            cv2.imwrite('{}/{}.jpg'.format(TMP_DIR, filename), frame)
            currentImages.append(frame)

        # Check for motion
        if len(currentImages) >= 2:
            if compareImages(currentImages[0], currentImages[1], DIFFERENCE_PERCENTAGE):
                saveImageCounter = imagesSavedAfterMotion
                print('=====MOTION DETECTED=====')
                currentImages = currentImages[2:]
            else:
                currentImages.pop(0)

        # Wait for a full second to pass
        while time() < t0 + 1:
            pass

    # When everything done, release the capture
    cap.release()