from flask import Flask
from flask import request
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import face_recognizer
import seat_belt_recognizer

app = Flask(__name__)

@app.route("/SeatBelt/Validator", methods=['POST'])
def seatbeltValidator():
    image = getImageFromRequestBody()
    quantityOfPeople = face_recognizer.getFacesQuantity(image)
    
    if(quantityOfPeople == 0):
        return 'true'

    print('Quantity of people: ' + str(quantityOfPeople))
    quantityOfUsingSeatBelt = seat_belt_recognizer.getQuantityOfUsingSeatBelt(image)

    print('Quantity of seatbeld: ' + str(quantityOfUsingSeatBelt))
    if(quantityOfPeople > quantityOfUsingSeatBelt):
        return 'false'
    else:
        return 'true'


def getImageFromRequestBody():
    requestBody = request.get_json()
    base64String = requestBody["Image"]
    imgdata = base64.b64decode(base64String)
    return np.asarray(Image.open(BytesIO(imgdata)))
