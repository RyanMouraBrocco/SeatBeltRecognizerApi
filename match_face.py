import cv2
import numpy as np
import os
from PIL import Image

faceDetect = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
path = 'dataset'


def saveNewFaces(userId, childId, imgs):
    userPath = path + "/" + str(userId)

    if(not os.path.exists(userPath)):
        os.makedirs(userPath)

    for img in imgs:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        sampleNum = 0
        for(x, y, w, h) in faces:
            sampleNum = sampleNum+1
            cv2.imwrite(userPath + "/Child."+str(childId)+"." +
                        str(sampleNum)+".jpg", gray[y:y+h, x:x+w])


def trainAllUserChilds(userId):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    userPath = path + "/" + str(userId)
    imagepaths = [os.path.join(userPath, f) for f in os.listdir(userPath)]
    faces = []
    childIds = []
    for imagepath in imagepaths:
        faceImg = Image.open(imagepath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        childId = int(os.path.split(imagepath)[-1].split('.')[1])
        faces.append(faceNp)
        childIds.append(childId)
        cv2.waitKey(10)
    newIds = np.array(childIds)
    recognizer.train(faces, newIds)
    recognizer.save('recognizer/'+str(userId)+'.yml')


def recognizeChilds(userId, image):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer/"+str(userId)+".yml")
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    recognizeChildIds = []
    for(x,y,w,h) in faces:
        id,conf=recognizer.predict(gray[y:y+h,x:x+w])
        recognizeChilds(id)

    return recognizeChildIds