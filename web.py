from flask import Flask, render_template,request
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
    link = "<h1>歡迎進入徐晣紘的網站</h1>"
    link += "<a href = /mis>課程</a><hr>"
    link += "<a href = /today>現在日期時間</a><hr>"
    link += "<a href = /me>關於我</a><hr>"
    link += "<a href = /welcome?u=zhehong&d=靜宜大學資管系>get</a><hr>"
    link += "<a href = /account>POST</a><hr>"
    return link

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/me")
def me():
    now = datetime.now()
    return render_template("about.html")


@app.route("/welcome", methods = ["GET"])
def welcome():
    user = request.values.get("u")
    d = request.values.get("d")
    return render_template("welcome.html", name = user,d = d)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

if __name__ == "__main__":
    app.run(debug=True)

