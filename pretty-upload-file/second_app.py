# coding:utf-8

from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask import Flask, request
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, 'static')

html = '''
    <!DOCTYPE html>
    <title>Demo</title>
    <h1>Another way to implement upload file</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="photo">
        <input type="submit" value="upload">
    </form>
'''

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


@app.route('/', methods=["POST", "GET"])
def upload_photo():
    if request.method == "POST" and "photo" in request.files:
        filename = photos.save(request.files["photo"])
        file_url = photos.url(filename)
        return html + "<br><img src=" + file_url + ">"
    return html


if __name__ == "__main__":
    app.run(debug=True)
