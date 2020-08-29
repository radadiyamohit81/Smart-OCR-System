import pytesseract
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

print('Model loaded. Check http://127.0.0.1:5000/')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        folder = os.path.join(app.config['TEMP_FOLDER'], str(os.getpid()))
        os.mkdir(folder)
        input_file = os.path.join(folder, secure_filename(f.filename))
        f.save(input_file)
        pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
        text = pytesseract.image_to_string(input_file)
        return text
    return None


if __name__ == '__main__':
    app.run(debug=True)
