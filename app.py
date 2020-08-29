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

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['TEMP_FOLDER'] = '/tmp'


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
            if not os.path.exists(os.path.join(app.config['TEMP_FOLDER'], str(os.getpid()))):
                folder = os.path.join(app.config['TEMP_FOLDER'], str(os.getpid()))
            else:
                shutil.rmtree(os.path.join(app.config['TEMP_FOLDER'], str(os.getpid())))
                # os.remove(os.path.join(app.config['TEMP_FOLDER'],str(os.getpid())))
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
