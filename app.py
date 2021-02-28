import numpy as np
import cv2
from flask import Flask, request, jsonify, render_template, redirect, make_response, url_for
import pickle
import math
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = "images/"
OUTPUT_FOLDER = "static/Done.jpg"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET','POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if uploaded_file.filename != '':
        uploaded_file.save(UPLOAD_FOLDER + filename)
        filepath = os.path.realpath(UPLOAD_FOLDER + filename)

    #img = cv2.imread('/home/sonu/Desktop/ML_project/ Image Into Sketch/images/images.jpeg', 1)
    img = cv2.imread(filepath, 1)
    # cv2.imshow("image", img)
    my_grey_dog = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    my_dog_bitwise = cv2.bitwise_not(my_grey_dog)
    my_dog_smooting = cv2.GaussianBlur(my_dog_bitwise, (21, 21), sigmaX=0, sigmaY=0)

    def dodgeV2(x, y):
        return cv2.divide(x, 255 - y, scale=256)

    final_img = dodgeV2(my_grey_dog, my_dog_smooting)
    #saving the output
    outt = cv2.imwrite('static/output/Done.jpg', final_img)
    # Displaying the image
    #cv2.imshow("image", final_img)
    #cv2.waitKey(5000)
    # closing all open windows
    #cv2.destroyAllWindows()

    return render_template('end.html', OUTPUT_FOLDER = final_img)


if __name__ == "__main__":
    app.run(debug=True)
