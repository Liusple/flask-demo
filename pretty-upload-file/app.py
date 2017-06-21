from flask import Flask, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, 'static')

FILE_TYPE = ['jpg', 'png', 'gif']

html='''
    <!DOCTYPE html>
    <title>Pretty Upload File</title>
    <h1>Pretty Upload File</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
'''

def verify_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in FILE_TYPE

@app.route('/uploaded/<filename>')
def getfile(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/', methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and verify_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            file_url = url_for('getfile', filename=filename)
            return html + '<img src=' + file_url + '>'
    return html


if __name__ == '__main__':
    app.run(debug=True)
