from flask import Flask, render_template,request
from datetime import datetime
import math
app = Flask(__name__)

@app.route("/")
def index():
    link = "<h1>歡迎進入徐晣紘的網站</h1>"
    link += "<a href = /mis>課程</a><hr>"
    link += "<a href = /today>現在日期時間</a><hr>"
    link += "<a href = /me>關於我</a><hr>"
    link += "<a href = /welcome?u=zhehong&d=靜宜大學資管系>get</a><hr>"
    link += "<a href = /account>POST</a><hr>"
    link += "<a href='/calculate'>次方與根號計算</a><hr>"
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

@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        try:
            # 取得數值
            base_num = float(request.form.get("base_num")) # 底數
            
            # 1. 處理次方
            exp_val = float(request.form.get("exp_val"))
            power_result = math.pow(base_num, exp_val)
            
            # 2. 處理開根號 (n 次方根)
            root_degree = float(request.form.get("root_degree"))
            if root_degree == 0:
                root_result = "次根數不可為 0"
            elif base_num < 0 and root_degree % 2 == 0:
                root_result = "負數無法開偶數次方根"
            else:
                # 核心公式：x 的 n 次方根 = x 的 (1/n) 次方
                root_result = math.pow(base_num, 1/root_degree)
            
            return f"""
                <h3>計算結果：</h3>
                <p>數字 {base_num} 的 {exp_val} 次方 = <b>{power_result}</b></p>
                <p>數字 {base_num} 的 {root_degree} 次根 = <b>{root_result}</b></p>
                <hr>
                <a href='/calculate'>重新計算</a> | <a href='/'>回首頁</a>
            """
        except ValueError:
            return "請輸入有效的數字！<a href='/calculate'>返回</a>"
            
    return render_template("calculate.html")
if __name__ == "__main__":
    app.run(debug=True)

