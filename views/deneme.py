from flask import Blueprint, render_template
from forms import RegisterForm

bp = Blueprint("deneme", __name__, template_folder="../templates", static_folder="../static")


@bp.route("/deneme")
def deneme():
    return render_template("index.html")