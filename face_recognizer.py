import cv2
import mediapipe as mp

faceDetect = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            
def getAllPeopleInImage(image):
    resultImages = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    imgH, imgW, imgC = image.shape
    for(x, y, w, h) in faces:
        resultImages.append(image[y - int(h/2) : imgH, x - w: x + (2 * w)])

    return resultImages