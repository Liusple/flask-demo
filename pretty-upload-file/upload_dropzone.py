# coding:utf-8

from flask import Flask, render_template, request
import os

app = Flask(__name__)

app.config["UPLOADED_PATH"] = os.getcwd() + "\\photo"


@app.route('/', methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        #must "file"
        for f in request.files.getlist("file"):
            f.save(os.path.join(app.config["UPLOADED_PATH"], f.filename))
    return render_template("upload_dropzone.html")

if __name__ == "__main__":
    app.run(debug=True)