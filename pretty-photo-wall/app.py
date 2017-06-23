from flask import Flask, request, render_template, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES
import os
import time
import hashlib
from wall import Wall

basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)
#must be PHTOTS
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, "static")

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST" and "photo" in request.files:
        dict = hashlib.md5(str(time.time()).encode("utf-8")).hexdigest()[:7]

        amount = len(request.files.getlist("photo"))
        print(dict, amount)
        print(app.config["UPLOADED_PHOTOS_DEST"])
        print(basedir)
        if amount in range(10, 100):
            for num, image in enumerate(request.files.getlist("photo")):
                filename = dict + str(num)
                photos.save(image, folder=dict, name=filename+".")
            return redirect(url_for("wall", dict=dict))
    return render_template("index.html")

@app.route("/wall/<dict>")
def wall(dict):
    wall = Wall(dict)
    images = wall.create()
    overview = wall.overview()
    return render_template("wall.html", images=images, overview=overview)



if __name__ == '__main__':
    app.run(debug=True)
