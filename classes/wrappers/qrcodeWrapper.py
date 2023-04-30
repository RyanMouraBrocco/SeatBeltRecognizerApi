import cv2

def readQRCodeValue(img):
    try:  
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return None

class QRCodeWrapper:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.image = img
        self.value = readQRCodeValue(img)