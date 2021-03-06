# coding=utf-8

from . import main
from .forms import EditProfileForm, PostForm, CommentForm, EditProfileAdminForm, BugForm
from flask import redirect, url_for,render_template, flash, abort, request, make_response
from flask_login import current_user, login_required
from .. import db
from ..models import User, Post, Comment, Permission, Role, Bug
from ..decorators import permission_required, admin_required


@main.route("/", methods=["POST", "GET"])
def index():
    form = PostForm()
    #permission
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(author=current_user._get_current_object(), body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash("Post success")
        return redirect(url_for("main.index"))
    show_followed = False
    if current_user.is_authenticated:##
        show_followed = bool(request.cookies.get("show_followed", ""))
    if show_followed:##
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get("page", 1, type=int)
    #Post.query.order_by()
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template("index.html", form=form, posts=posts, pagination=pagination, show_followed=show_followed)


@main.route("/edit-profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data  #if empty
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash("Edit profile success")
        return redirect(url_for("main.user", username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", form=form)


@main.route("/edit-profile/<int:id>", methods=["POST", "GET"])
@login_required
@admin_required
def admin_edit_profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user) ##not user
    if form.validate_on_submit():
        user.username = form.username.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.role = Role.query.get(form.role.data)#####
        db.session.add(user)
        db.session.commit()
        flash("Profile update success")
        return redirect(url_for("main.user", username=user.username))#username=
    form.username.data = user.username
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.role.data = user.role_id####
    return render_template("edit_profile.html", form=form)


@main.route("/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get("page", 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template("user.html", user=user, posts=posts, pagination=pagination)


@main.route("/post/<int:id>", methods=["POST", "GET"])
def post(id):
    post = Post.query.get_or_404(id)    #
    form = CommentForm()
    #在html控制评论是否可以评论
    if form.validate_on_submit():
        ##current_user._get_current_object()
        comment = Comment(body=form.body.data, author=current_user._get_current_object(), post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Comment success")
        return redirect(url_for("main.post", id=post.id, page=-1))##post.id
    page = request.args.get("page", 1, type=int)
    #if page == -1
    if page == -1:
        page = (post.comments.count() - 1) // 20 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=20, error_out=False)              ##
    comments = pagination.items
    return render_template("post.html", posts=[post], comments=comments, pagination=pagination, form=form)


@main.route("/edit-post/<int:id>", methods=["POST", "GET"])
@login_required
def edit_post(id):
    #需要在这边控制谁可以修改post，因为可以输入url
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash("Edit success")
        return redirect(url_for("main.post", id=post.id))
    form.body.data = post.body
    return render_template("edit_post.html", form=form)


@main.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for("main.index"))
    if current_user.is_following(user):
        flash("You are already following this user")
        return redirect(url_for("main.user", username=username))
    current_user.follow(user)
    flash("Follow success")
    return redirect(url_for("main.user", username=username))

@main.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for("main.index"))
    if not current_user.is_following(user):
        flash("You are not following this user")
        return redirect(url_for("main.user", username=username))
    current_user.unfollow(user)
    flash("Unfollow success")
    return redirect(url_for("main.user", username=username))


@main.route("/followers/<username>")
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)
    pagination = user.followers.paginate(page, per_page=20, error_out=False)
    follows = [{"user":item.follower, "time":item.timestamp} for item in pagination.items]###
    return render_template("follows.html", pagination=pagination, endpoint="main.followers", follows=follows, user=user, title="Followers")


@main.route("/followed/<username>")
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for("main.index"))
    page = request.args.get("page", 1, type=int)
    #user.followed
    pagination = user.followed.paginate(page, per_page=20, error_out=False)
    follows = [{"user":item.followed, "time":item.timestamp} for item in pagination.items]
    return render_template("follows.html", pagination=pagination, endpoint="main.followed", follows=follows, user=user, title="Following")

@main.route("/all")
@login_required
def show_all():
    resp = make_response(redirect(url_for("main.index")))###
    resp.set_cookie("show_followed", "", max_age=30*24*60*60)
    return resp

@main.route("/followed")
@login_required
def show_followed():
    resp = make_response(redirect(url_for("main.index")))
    resp.set_cookie("show_followed", "1", max_age=30*24*60*60)
    return resp

@main.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get("page", 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    comments = pagination.items
    return render_template("moderate.html", comments=comments, pagination=pagination, page=page)


@main.route("/moderate/enable/<int:id>")
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("main.moderate", page=request.args.get("page", 1, type=int)))


@main.route("/moderate/disable/<int:id>")
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("main.moderate", page=request.args.get("page", 1, type=int)))

@main.route("/report-bug", methods=["POST", "GET"])
def report_bug():
    form = BugForm()
    if form.validate_on_submit():
        bug = Bug(body=form.body.data)
        if current_user.is_authenticated:
            bug.author = current_user._get_current_object()
        else:
            bug.author = User.query.filter_by(username="bug").first()
        db.session.add(bug)
        db.session.commit()
        flash("Report bug success")
        return redirect(url_for("main.report_bug"))
    return render_template("report_bug.html", form=form)


@main.route("/show-bugs")
@login_required
@admin_required
def show_bugs():
    ##
    bugs = Bug.query.order_by(Bug.timestamp.desc()).all()
    return render_template("show_bugs.html", bugs=bugs)
