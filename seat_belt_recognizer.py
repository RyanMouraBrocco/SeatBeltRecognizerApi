#   Seat Belt Detection Using Opencv And Python Based On Line Detection
#   Coder: Syed Naveed Abbas
#   Email: programmingconcepts101@gmail.com


import cv2
import numpy as np
import imutils

from PIL import Image
import requests
from io import BytesIO


def Slope(a, b, c, d):
    return (d - b)/(c - a)


def getImage():
    response = requests.get(
        "https://grillo.ca/wp-content/uploads/2017/09/seat-belt.jpg")
    return np.asarray(Image.open(BytesIO(response.content)))


# Reading Image

beltframe = getImage()


def getQuantityOfUsingSeatBelt(image):
    # Converting To GrayScale
    beltgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # No Belt Detected Yet
    belt = 0

    # Bluring The Image For Smoothness
    blur = cv2.blur(beltgray, (1, 1))

    # Converting Image To Edges
    edges = cv2.Canny(blur, 50, 400)


    # Previous Line Slope
    ps = 0

    # Previous Line Co-ordinates
    px1, py1, px2, py2 = 0, 0, 0, 0

    # Extracting Lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/270, 30,
                            maxLineGap=20, minLineLength=170)

    # If "lines" Is Not Empty
    if lines is not None:

        # Loop line by line
        for line in lines:

            # Co-ordinates Of Current Line
            x1, y1, x2, y2 = line[0]

            # Slope Of Current Line
            s = Slope(x1, y1, x2, y2)

            # If Current Line's Slope Is Greater Than 0.7 And Less Than 2
            if ((abs(s) > 0.7) and (abs(s) < 2)):

                # And Previous Line's Slope Is Within 0.7 To 2
                if((abs(ps) > 0.7) and (abs(ps) < 2)):

                    # And Both The Lines Are Not Too Far From Each Other
                    if(((abs(x1 - px1) > 5) and (abs(x2 - px2) > 5)) or ((abs(y1 - py1) > 5) and (abs(y2 - py2) > 5))):
                        # Belt Is Detected
                        print("Belt Detected")
                        belt += 1

            # Otherwise Current Slope Becomes Previous Slope (ps) And Current Line Becomes Previous Line (px1, py1, px2, py2)
            ps = s
            px1, py1, px2, py2 = line[0]


    return belt
