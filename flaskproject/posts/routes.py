from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskproject import db
from flaskproject.models import Post
from flaskproject.posts.forms import PostForm, SearchForm

# each blueprint is an isolated part of the functionality of our project
# the blueprint class will use the name var to determine paths to all files of the blueprint
posts = Blueprint("posts", __name__, template_folder="templates")


@posts.route("/post/new", methods=["GET", "POST"])
# to post the user should be logedin
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # adding the post into the db
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.app_context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# create seearch function
@posts.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        # Get data from submitted form
        post.searched = form.searched.data
        # Query the Database
        posts = posts.filter(Post.title.like("%" + post.searched + "%"))
        posts = posts.order_by(Post.title).all()

        return render_template(
            "search.html", form=form, searched=post.searched, posts=posts
        )


# update and edit posts
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(
        post_id
    )  # give the post with this id if exist or 404 if doesn't
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # 403:You don't have the permission to access the requested resource
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
