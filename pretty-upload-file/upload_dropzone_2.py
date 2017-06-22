# coding:utf-8
# use flask_dropzone

from flask_dropzone import Dropzone
from flask import Flask, request, render_template
import os

app = Flask(__name__)
dropzone = Dropzone(app)

app.config["UPLOAD_PATH"] = os.getcwd() + "\\photo"
app.config.update(
    DROPZONE_ALLOWED_FILE_TYPE="image",
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_INPUT_NAME="photo",
    DROPZONE_MAX_FILES=30
)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        #here "photos"
        for f in request.files.getlist("photo"):
            f.save(os.path.join(app.config["UPLOAD_PATH"], f.filename))
    return render_template("upload_dropzone_2.html")


if __name__ == "__main__":
    app.run(debug=True)
