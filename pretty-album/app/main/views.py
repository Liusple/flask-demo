# coding:utf-8

from flask import render_template, flash, redirect, request, abort, url_for
from . import main
from flask_login import login_required
from .forms import EditProfileForm, EditProfileAdminForm, NewAlbumForm, CommentForm
from ..models import User, Role, Album, Photo, Comment, Message
from flask_login import current_user
from .. import db
from ..decorators import admin_required, permission_required

@main.route("/")
def index():
    flash(request.endpoint, "info")
    return render_template("index.html")


@main.route("/secret")
@login_required
def secret():
    return render_template("test.html")


@main.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(403)
    return render_template("user.html", user=user)


@main.route("/edit-profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.status = form.status.data
        db.session.add(current_user)
        db.session.commit()
        flash(u"资料更新成功", "success")
        return redirect(url_for("main.user", username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.status.data = current_user.status
    return render_template("edit_profile.html", form=form)


@main.route("/edit-profile/<int:id>", methods=["POST", "GET"])
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)###
    if user is None:
        abort(403)
    form = EditProfileAdminForm(user=user)##need user=user
    if form.validate_on_submit():
        user.email = form.email.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.status = form.status.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)###
        #必要漏了db
        flash(u"用户资料更新成功", "success")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.user", username=user.username))
    form.about_me.data = user.about_me
    form.location.data = user.location
    form.email.data = user.email
    form.status.data = user.status
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id###
    return render_template("edit_profile.html", form=form)


@main.route("/new-album", methods=["POST", "GET"])
@login_required
def new_album():
    form = NewAlbumForm()
    if form.validate_on_submit():
        #images = []
       # if request.method == "POST" and "photo" in request.files:
            #images = save_image(request.files.getlist("photo"))
        title = form.title.data
        about = form.about.data
        author = current_user._get_current_object()##
        no_public = form.no_public.data
        no_comment = form.no_comment.data
        album = Album(author=author, title=title, about=about, no_public=no_public, no_comment=no_comment)
        db.session.add(album)

        #for url in images:
           # photo = Photo(url=url[0], url_s=url[1], url_t=url[2], album=album, author=current_user._get_current_object())
            #db.session.add(photo)
        db.session.commit()
       # return redirect(url_for("main.edit_photo", id=album.id))
        flash(u"相册创建成功", "success")
        return redirect(url_for("main.index"))
    return render_template("new_album.html", form=form)


@main.route("/<username>", methods=["POST", "GET"])
def albums(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get("page", 1, type=int)
    pagination = user.albums.order_by(Album.timestamp.desc()).paginate(
        page, per_page=20, error_out=False)
    albums = pagination.items

    photo_count = sum([len(album.photos.all()) for album in albums])##
    album_count = len(albums)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Message(body=form.body.data,
                          user=user,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash(u"评论成功")
        return redirect(url_for("main.albums", username=username))
    comments = user.messages.order_by(Message.timestamp.desc()).all()
    return render_template("albums.html", form=form, comments=comments,
                           user=user, albums=albums, album_count=album_count,
                           photo_count=photo_count, pagination=pagination)

@main.route("/album/<int:id>")
def album(id):
    album = Album.query.get_or_404(id)
    placeholder = ""
    photo_amount = len(list(album.photos))
    if photo_amount == 0:
        album.cover = placeholder
    elif photo_amount != 0 and album.cover == placeholder:
        album.cover = album.photos[0].path

    if current_user != album.author and album.no_public == True:
        abort(404)

    page = request.args.get("page", 1, type=int)
    ##
    pagination = album.photos.order_by(Photo.order.asc()).paginate(
        page, 20, error_out=False)
    photos = pagination.items

    if len(photos) == 0:
        no_pic = True
    else:
        no_pic = False

    return render_template("album.html", album=album, photos=photos, pagination=pagination, no_pic=no_pic)