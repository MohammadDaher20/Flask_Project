from flask import Blueprint, render_template, request
from flaskproject.models import Post

# each blueprint is an isolated part of the functionality of our project
main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About Page")


@main.route("/announcements")
def announcements():
    return render_template("announcements.html", title="Announcement Page")
