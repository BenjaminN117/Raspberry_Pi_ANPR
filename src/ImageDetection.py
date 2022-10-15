'''
Product: Raspberry Pi ANPR
Description: Local number plate detection script
Author: Benjamin Norman
Creation Date: 2022
'''

import imutils
from NumberPlateChecker import NumberPlateChecker

class Plate_Detection():
    def __init__(self, usbDevName):
        self.usbDevName = usbDevName

    # CV2 plate detection, only detects if there is a number plate in the image
    def plate_detection():
        img = cv2.imread('1.jpg', cv2.IMREAD_COLOR)

        img = cv2.resize(img, (620, 480))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None

        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            print("No number plate detected")
            
        else:
            print("Found a number plate!!")
            print("Sending to Sight Hound")
            Sighthound()

    #Image triggering goes here

    plate_detection()
