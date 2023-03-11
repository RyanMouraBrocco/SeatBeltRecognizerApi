from flask import Flask, jsonify
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
    image = getImageFromRequestBody()
    quantityOfPeople = face_recognizer.getFacesQuantity(image)

    if(quantityOfPeople == 0):
        return 'true'

    print('Quantity of people: ' + str(quantityOfPeople))
    quantityOfUsingSeatBelt = seat_belt_recognizer.getQuantityOfUsingSeatBelt(
        image)

    print('Quantity of seatbeld: ' + str(quantityOfUsingSeatBelt))
    if(quantityOfPeople > quantityOfUsingSeatBelt):
        return 'false'
    else:
        return 'true'


# USERS
def getUserFromBody():
    requestBody = request.get_json()
    return User(0, requestBody["Name"], requestBody["Email"], requestBody["Password"], requestBody["CityId"])


@app.route("/Users", method=['POST'])
def PostUser():
    user = getUserFromBody()
    conn = sqllite_access.createIfNotDatabase()
    userCheck = sqllite_access.getUserByEmail(conn, user.email)
    if(userCheck != None):
        sqllite_access.closeConnection(conn)
        return (401, 'Email already inserted')

    user = sqllite_access.insertUser(conn, user)
    sqllite_access.closeConnection(conn)
    return jsonify(user)


@app.route("/Users/Login", method=['POST'])
def Login():
    requestBody = request.get_json()
    email = requestBody["Email"]
    password = requestBody["Password"]
    conn = sqllite_access.createIfNotDatabase()
    userCheck = sqllite_access.getUserByEmail(conn, email)
    if(userCheck == None or userCheck.password != password):
        sqllite_access.closeConnection(conn)
        return (401, 'Email or password is wrong')

    newKey = random.getrandbits(128)
    sqllite_access.updateUserKey(conn, userCheck.Id, newKey)
    sqllite_access.closeConnection(conn)
    return


# Child
def getChildFromBody(userId):
    requestBody = request.get_json()
    return Child(0, userId, requestBody["Name"])


@app.route("/Childs", method=['POST'])
def PostChild():
    authenticatededUser = authenticateUser()
    if(authenticatededUser == None):
        return (401, "User not authenticated")

    child = getChildFromBody(authenticatededUser.id)
    conn = sqllite_access.createIfNotDatabase()
    child = sqllite_access.insertChild(conn, child)
    sqllite_access.closeConnection(conn)
    return jsonify(child)


@app.route("/Childs/<childId>/UploadImage", method=['POST'])
def AddChildImage(childId):
    authenticatededUser = authenticateUser()
    if(authenticatededUser == None):
        return (401, "User not authenticated")

    image = getImageFromRequestBody()
    conn = sqllite_access.createIfNotDatabase()

    allChilds = sqllite_access.getAllChildsByUserId(
        conn, authenticatededUser.id)

    isValidChild = False
    validChild = None
    for child in allChilds:
        if(child.id == child):
            isValidChild = True
            validChild = child
            break

    if(isValidChild):
        match_face.saveNewFace(authenticatededUser.id,
                               childId, image, validChild.imageQuantity)
        sqllite_access.UpdateChildImageQuantity(conn,
                                                childId, validChild.imageQuantity + 1)
        sqllite_access.closeConnection(conn)
    else:
        sqllite_access.closeConnection(conn)
        return (401, "Child is not valid")


@app.route("/Childs/Train", method=['POST'])
def TrainChildImage():
    authenticatededUser = authenticateUser()
    if(authenticatededUser == None):
        return (401, "User not authenticated")
    
    match_face.trainAllUserChilds(authenticatededUser.Id)