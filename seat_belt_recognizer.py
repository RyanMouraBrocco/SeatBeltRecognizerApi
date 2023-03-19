import cv2
import numpy as np
import imutils

from PIL import Image
import requests
from io import BytesIO


def Slope(a, b, c, d):
    return (d - b)/(c - a)


def getQuantityOfUsingSeatBelt(image):
    beltgray = cv2.cvtColor(image, cv2.IMWRITE_PAM_FORMAT_BLACKANDWHITE)
    blur = cv2.blur(beltgray, (1, 1))
    belt = 0

    edges = cv2.Canny(blur, 50, 600)
    lines = cv2.HoughLinesP(edges, 1, np.pi/270, 70,
                            maxLineGap=50, minLineLength=150)

    previousLineSlope = 0
    previousX1, previousY1, previousX2, previousY2 = 0, 0, 0, 0
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            s = Slope(x1, y1, x2, y2)

            if ((abs(s) > 1.5) and (abs(s) < 6)):
                if(len(lines) == 1 or ((abs(previousLineSlope) > 1.5) and (abs(previousLineSlope) < 6))):
                    if(((abs(x1 - previousX1) > 5) and (abs(x2 - previousX2) > 5)) or ((abs(y1 - previousY1) > 5) and (abs(y2 - previousY2) > 5))):
                        belt += 1

            previousLineSlope = s
            previousX1, previousY1, previousX2, previousY2 = line[0]

    return belt
