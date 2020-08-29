import pytesseract
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
        text = pytesseract.image_to_string(file_path)
        return text
    return None


if __name__ == '__main__':
    app.run(debug=True)
