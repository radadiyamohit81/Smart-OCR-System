try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import shutil
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

print('Check http://127.0.0.1:5000/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '/uploads/'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            f.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, f.filename))
            pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
            text = pytesseract.image_to_string(f)
            return text
    return None


if __name__ == '__main__':
    app.run(debug=True)
