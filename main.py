import os
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'webp', 'jpg'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def processImage(filename, operation):
    print(f"the filename {filename} was performed an operation {operation}")
    img = cv2.imread(f"./uploads/{filename}")
    match operation:
        case 'cgray': 
            # using cvtColor (convert color) of cv2 library to do manipulations
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            newFilename = f"./static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case 'cwebp': 
            # using filename . to split and change the format
            newFilename = f"./static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case 'cjpg': 
            # using filename . to split and change the format
            newFilename = f"./static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case 'cpng': 
            # using filename . to split and change the format
            newFilename = f"./static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass

@app.route('/')
def home():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# to upload images
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "there was an error in uploading the file"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "please select a file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"{filename} was processed. Click <a href='./{new}' target='_blank'>here</a> to view your processed image.")
            return render_template("index.html")
    return render_template('index.html')

app.run(debug=True, port = 5001)