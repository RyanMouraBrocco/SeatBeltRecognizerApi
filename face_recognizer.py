import cv2
import mediapipe as mp

def getFacesQuantity(image):
    faceDetectionSolution = mp.solutions.face_detection
    faceDetector = faceDetectionSolution.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    
    facesList = faceDetector.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if(not facesList.detections):
        facesList = faceDetector.process(image)

    if(not  facesList.detections):
        return 0
    else:
        return len(facesList.detections)
