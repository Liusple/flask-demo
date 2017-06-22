# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileAllowed, FileRequired, FileField
from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, patch_request_class, configure_uploads, IMAGES
import os
import hashlib
import time

basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "forever young"
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, 'photo')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Only photo can be uploaded.'), FileRequired('Not choice photo')])
    submit = SubmitField('upload')


@app.route('/', methods=["POST", "GET"])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):

            name = hashlib.md5(('admin' + str(time.time())).encode("utf-8")).hexdigest()[:15]
            photos.save(filename, name=name + '.')
        success = True
    else:
        success = False
    return render_template('index.html', form=form, success=success)


@app.route('/manager')
def manager():
    photo_list = os.listdir(app.config["UPLOADED_PHOTOS_DEST"])
    return render_template('manager.html', photo_list=photo_list)


@app.route('/open/<photoname>')
def open(photoname):
    photo_url = photos.url(photoname)
    return render_template('photo.html', photo_url=photo_url)


@app.route('/delete/<photoname>')
def delete(photoname):
    photopath = photos.path(photoname)
    os.remove(photopath)
    print(photopath)
    return redirect(url_for('manager'))


if __name__ == '__main__':
    app.run(debug=True)
