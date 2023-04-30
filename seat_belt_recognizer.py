import cv2
import numpy as np
from classes.wrappers.qrcodeWrapper import QRCodeWrapper


def getQuantityOfUsingSeatBelt(image):
    belt = 0

    qrCodes = getQRCodesInImage(image)
    if(len(qrCodes) >= 3):
        qrCodeCheck = 0
        for qrCode in qrCodes:
            if(qrCode.value == "https://me-qr.com/text/3035980/show"):
                if(qrCodeCheck == 2):
                    belt+=1
                    qrCodeCheck = 0
                else:
                    qrCodeCheck += 1
    
    return belt

def getQRCodesInImage(image):
    imageCopy = image.copy()
    gray = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    qrCodes = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv2.rectangle(imageCopy, (x, y), (x + w + 10, y + h + 10), (36,255,12), 3)
            qrcodeImg = image[y-10:y+h+10, x-10:x+w+10]
            qrCodes.append(QRCodeWrapper(x, y, w, h, qrcodeImg))

    return qrCodes
