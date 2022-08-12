from flask import Flask, redirect,url_for,render_template,session, request
from datetime import datetime
from dbTable import *
from settings import app,db

@app.route("/test")
def test():
    return "<h1>test<h1>"

@app.route("/", methods=["POST","GET"])
def Login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        password = request.form["password"]
        session_username = UserInfo.query.filter_by(username=user).first()
        session_password = UserInfo.query.filter_by(password=password).first()
        if session_username and session_password:
           session["user"] = user
           return redirect(url_for("User"))
        else:
            return redirect(url_for("Login"))
    else:
        if "user" in session:
            return redirect(url_for("User"))
        else:
            return render_template("login.html")

@app.route("/register", methods=["POST","GET"])
def Register():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        Add_User = UserInfo(user,password)
        db.session.add(Add_User)
        db.session.commit()
        return redirect(url_for("Register"))
    else:
        return render_template("Register.html")

@app.route("/user", methods=["POST","GET"])
def User():
    if "user" in session:
        if request.method == "POST":
            username_key = request.form["username_key"]
            found_user = UserInfo.query.filter_by(username=username_key).first()
            return redirect(url_for("Search_User", usr=found_user.username))
        else:
            user_list = UserInfo.query.all()
            return render_template("user.html", values=user_list, total=len(user_list), current_user=session["user"])
    else:
        return redirect(url_for("Login"))


@app.route("/user/search/<usr>")
def Search_User(usr):
    if "user" in session:
        user_list = UserInfo.query.all()
        return render_template("search_user.html", values=user_list, user_key=usr)
    else:
        return redirect(url_for("Login"))

@app.route("/delete-user<_id>")
def Delete_User(_id):
    if "user" in session:
        user = UserInfo.query.filter_by(_id=_id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("User"))
    else:
        return redirect(url_for("Login"))

@app.route("/chat", methods=["POST","GET"])
def Global_Chat():
    if "user" in session:
        if request.method == "POST":
            msg = request.form["message"]
            now = datetime.now()
            date_time = now.strftime("%m/%d/%y %H:%M")
            new_message = MessageHistory(session["user"],msg,date_time)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for("Global_Chat"))
        else:
            message_list = MessageHistory.query.all()
            return render_template("chat.html", values=message_list, current_user = session["user"])
    else:
        return redirect(url_for("Login"))
@app.route("/test<message>")
def test_message(message):
    return f"<h1>{message}<h1>"

@app.route("/logout")
def Logout():
        session.pop("user", None)
        return redirect(url_for("Login"))

if __name__ == "__main__":
    app.run(debug=True)