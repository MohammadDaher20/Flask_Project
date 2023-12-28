from flask import render_template, request, flash, url_for, redirect, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flaskproject import db, bcrypt
from flaskproject.models import User, Post
from flaskproject.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskproject.users.utils import save_picture

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    # if the user has logedin the click on the login/register label will redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        # Create the db first
        # db.create_all()
        db.session.add(user)
        db.session.commit()
        # one time alert message using flash()
        flash("Your account has been created! You are now able to login", "success")
        # to go back to the home page we use redirect('link of the home page ')
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    # if the user has logedin the click on the login/register label will redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if the user exist and the pass is verefied
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsucces. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
# if the user check acc page before logingin,will be redirected to the login page to login before
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file
    )  # image file is the name of the column where we store our image on the user model
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_posts.html", posts=posts, user=user)
