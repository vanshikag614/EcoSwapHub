
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import requests
from werkzeug.utils import secure_filename

# Disable scientific notation for clarity
def pred(filePath):
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("new_model.h5", compile=False)

    # Load the labels
    class_names = {0 : 'glass', 1 : 'light bulbs', 2 : 'organic', 3 : 'clothes', 4 : 'batteries', 5 : 'paper', 6 : 'e-waste', 7 : 'plastic', 8 : 'metal'}


    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 100, 100, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(filePath).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (100, 100)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 255.0) 

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction,axis=1)
    class_name = class_names[index[0]]
    #confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    #print("Confidence Score:", confidence_score)
    return class_name

#app.py

app = Flask(__name__,static_url_path='/static')

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
file_arr = []
pred_class_arr = []
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/model')
def model():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file1' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file1 = request.files['file1']
    if file1.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file1 and allowed_file(file1.filename):
        filename1 = secure_filename(file1.filename)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        # print('upload_image filename: ' + filename)
        #flash('Image successfully uploaded and displayed below')
        # flash('\n FileName = '+filename)
        f1 = UPLOAD_FOLDER+filename1
        print('FileName1 = '+filename1)
        #Processing the images
        pred_class = pred(file1)
        pred_class_arr.append(pred_class)
        flash("It is a "+pred_class+" waste")
        file_arr.append(filename1)
        return render_template('index.html', filename1=filename1)

    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle login logic here
    return render_template('index.html')



@app.route('/page1')
def page1():
    # Stop the Flask server process
    shutdown_server()

    # Redirect to the PHP page served by XAMPP
    return redirect('http://localhost/proj/templates/page1.php')

def shutdown_server():
    # Get the process ID of the Flask server
    pid = os.getpid()

    # Terminate the Flask server process
    os.kill(pid, 2)  # 2 corresponds to the SIGINT signal (similar to Ctrl+C)



if __name__ == "__main__":
    app.debug = True
    app.run()