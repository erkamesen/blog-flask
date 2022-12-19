from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user



def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


def email_check(email):
    symbol_count = email.count("@")
    if symbol_count == 1:
        disallowed_characters = ["!","#","$","%","&","'","*","+","-","/","=","?","^","_","`","{","|","}","~","İ","Ö","ç","ğ","ö","ş","ı","Ğ","Ç","ü","Ü","@"]
        for character in email:
            if character in disallowed_characters:
                flash("Lütfen geçerli bir email giriniz.")
                return redirect(url_for("user.register"))
        else:
            return True