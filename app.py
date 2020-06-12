from flask import Flask, request
from flask_restful import Resource, Api
import random
from flask_cors import CORS
import os
from cv2 import CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY, rectangle, waitKey
from pricepredictor import predict_price

app = Flask(__name__)
CORS(app)

api = Api(app)

MYDIR = os.path.dirname(__file__)
app.config["IMAGE_UPLOADS"] = MYDIR+"/Uploads"

face_cascade = CascadeClassifier('haarcascade_frontalface_default.xml')


class FaceDetection(Resource):
    def get(self):
        return { 'about': 'Hello' }
    def post(self):
        if request.files:
            name = random.randint(1,1000)
            image = request.files["images"]
            image.save(os.getcwd()+"/Uploads/"+ str(name)+".jpg")
            img = imread(os.getcwd()+"/Uploads/"+ str(name)+".jpg")
            gray = cvtColor(img, COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            # print("faces <<<<< ", all(faces))
            # print("what is faces ",faces.size) faces.size != 0 or
            # gotta figure out how to check if numpy and tuple are empty
            if faces is not '':
                return "You are a human Being. Enjoy your login"

            for (x, y, w, h) in faces:
                rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

            waitKey()
        else:
            return "You are not a human being"

class PricePrediction(Resource):
    def get(self):
        return predict_price('Feb 20, 2019', 1000)
api.add_resource(FaceDetection, '/')
api.add_resource(PricePrediction, '/priceprediction')
if __name__ == '__main__':
    app.run(debug=True)