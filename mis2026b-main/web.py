from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
    link = "<h1>歡迎進入徐晣紘的網站</h1>"
    link += "<a href = /mis>課程</a><hr>"
    link += "<a href = /today>現在日期時間</a><hr>"
    link += "<a href = /me>關於我</a><hr>"
    link += "<a href = /welcome>get</a><hr>"
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

@app.route("/welcome")
def welcome():
    return render_template("welcome.html",name = "hong")


if __name__ == "__main__":
    app.run(debug=True)

