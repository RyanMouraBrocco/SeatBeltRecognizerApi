from flask import Flask, abort, jsonify
from flask import request
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import face_recognizer
import seat_belt_recognizer
from classes.child import Child
from classes.user import User
import sqllite_access
import random
import match_face
import cv2

app = Flask(__name__)

# AUTHENTICATION


def authenticateUser():
    key = request.headers.get('auth')
    conn = sqllite_access.createIfNotDatabase()
    authenticatedUser = sqllite_access.getUserByKey(conn, key)
    sqllite_access.closeConnection(conn)
    return authenticatedUser


# SEAT BELT
def getImageFromRequestBody():
    requestBody = request.get_json()
    base64String = requestBody["Image"]
    imgdata = base64.b64decode(base64String)
    return np.asarray(Image.open(BytesIO(imgdata)))


@app.route("/SeatBelt/Validator", methods=['POST'])
def seatbeltValidator():
    authenticatededUser = authenticateUser()
    if(authenticatededUser == None):
        return (401, "User not authenticated")

    image = getImageFromRequestBody()
    cv2.imwrite("test.jpg", image)
    allPeopleImages = face_recognizer.getAllPeopleInImage(image)

    if(len(allPeopleImages) == 0):
        return 'true'

    childsInDangerSituation = 0
    for img in allPeopleImages:
        cv2.imwrite("test2.jpg", img)
        childIds = match_face.recognizeChilds(authenticatededUser.id, img)
        if(len(childIds) > 0):
            quantityOfSeatBelt = seat_belt_recognizer.getQuantityOfUsingSeatBelt(
                img)
            if(quantityOfSeatBelt < len(childIds)):
                childsInDangerSituation += len(childIds)

    if(childsInDangerSituation > 0):
        return 'false'
    else:
        return 'true'


# USERS
def getUserFromBody():
    requestBody = request.get_json()
    return User(0, requestBody["Name"], requestBody["Email"], requestBody["Password"], requestBody["CityId"])


@app.route("/Users", methods=['POST'])
def PostUser():
    user = getUserFromBody()
    conn = sqllite_access.createIfNotDatabase()
    userCheck = sqllite_access.getUserByEmail(conn, user.email)
    if(userCheck != None):
        sqllite_access.closeConnection(conn)
        abort(401, 'Email already inserted')

    user = sqllite_access.insertUser(conn, user)
    sqllite_access.closeConnection(conn)
    return jsonify(user.serialize())


@app.route("/Users/Login", methods=['POST'])
def Login():
    requestBody = request.get_json()
    email = requestBody["Email"]
    password = requestBody["Password"]
    conn = sqllite_access.createIfNotDatabase()
    userCheck = sqllite_access.getUserByEmail(conn, email)
    if(userCheck == None or userCheck.password != password):
        sqllite_access.closeConnection(conn)
        abort(401, 'Email or password is wrong')

    newKey = str(random.getrandbits(128))
    sqllite_access.updateUserKey(conn, userCheck.id, newKey)
    sqllite_access.closeConnection(conn)
    return newKey


# Child
def getChildFromBody(userId):
    requestBody = request.get_json()
    return Child(0, userId, requestBody["Name"])


@app.route("/Childs", methods=['POST'])
def PostChild():
    authenticatededUser = authenticateUser()
    if(authenticatededUser == None):
        abort(401, "User not authenticated")

    child = getChildFromBody(authenticatededUser.id)
    conn = sqllite_access.createIfNotDatabase()
    child = sqllite_access.insertChild(conn, child)
    sqllite_access.closeConnection(conn)
    return jsonify(child.serialize())


@app.route("/Childs/<childId>/UploadImage", methods=['POST'])
def AddChildImage(childId):
    childId = int(childId)
    authenticatededUser = authenticateUser()
    if(authenticatededUser == None):
        abort(401, "User not authenticated")

    image = getImageFromRequestBody()
    conn = sqllite_access.createIfNotDatabase()

    allChilds = sqllite_access.getAllChildsByUserId(
        conn, authenticatededUser.id)

    isValidChild = False
    validChild = None
    for child in allChilds:
        if(child.id == childId):
            isValidChild = True
            validChild = child
            break

    if(isValidChild):
        match_face.saveNewFace(authenticatededUser.id,
                               childId, image, validChild.imageQuantity)
        sqllite_access.updateChildImageQuantity(conn,
                                                childId, validChild.imageQuantity + 1)
        sqllite_access.closeConnection(conn)
        return ""
    else:
        sqllite_access.closeConnection(conn)
        abort(401, "Child is not valid")


@app.route("/Childs/Train", methods=['POST'])
def TrainChildImage():
    authenticatededUser = authenticateUser()
    if(authenticatededUser == None):
        abort(401, "User not authenticated")

    match_face.trainAllUserChilds(authenticatededUser.id)
    return ""
