import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from datetime import datetime
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import math

# 1. 判斷環境並初始化 Firebase
if os.path.exists('serviceAccountKey.json'):
    cred = credentials.Certificate('serviceAccountKey.json')
else:
    firebase_config = os.getenv('FIREBASE_CONFIG')
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# 2. 初始化 Flask (原本漏掉這行)
app = Flask(__name__)

@app.route("/")
def index():
    link = "<h1>歡迎進入徐晣紘的網站20260409</h1>"
    link += "<a href='/mis'>課程</a><hr>"
    link += "<a href='/today'>現在日期時間</a><hr>"
    link += "<a href='/me'>關於我</a><hr>"
    link += "<a href='/welcome?u=zhehong&d=靜宜大學資管系'>get</a><hr>"
    link += "<a href='/account'>POST</a><hr>"
    link += "<a href='/calculate'>次方與根號計算</a><hr>"
    link += "<a href='/read'>讀取Firestore資料(靜宜資管)</a><hr>"
    link += "<a href='/read1'>關鍵字查詢(資管二B)</a><hr>"
    link += "<a href='/spider'>爬蟲w8(爬取子卿老師的課程)</a><hr>"
    link += "<a href='/movie1'>爬取即將上映的電影</a><hr>"
    link += "<a href='/spidermovie'>進入資料庫的電影</a><hr>"
    link += "<a href='/searchMovie'>電影搜尋系統</a><hr>"
    link += "<a href='/road'>台中市十大肇事原因</a><hr>"     
    return link

@app.route("/road")
def road():
    R = "台中市十大肇事路口(113年10月)"
    url ="https://datacenter.taichung.gov.tw/swagger/OpenData/a1b899c0-511f-4e3d-b22b-814982a97e41"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    Data = requests.get(url)
    JsonData = json.loads(Data.text)
    for item in JsonData:
        R += item["路口名稱"] + "原因:" + item["主要肇因"] +"<br?"
    return R

@app.route("/searchMovie", methods=["GET", "POST"])
def searchMovie():
    html_content = """
    <form method="post" action="/searchMovie">
        請輸入欲查詢的片名：
        <input type="text" name="MovieTitle" />
        <button type="submit">確定送出</button>
    </form>
    <hr>
    """

    if request.method == "POST":
        keyword = request.form.get("MovieTitle", "").strip()
        if keyword:
            db = firestore.client()
            docs = db.collection("電影2B").get()
            
            found_count = 0
            result_html = ""
            
            for doc in docs:
                movie = doc.to_dict()
                title = movie.get("title", "")
                
                if keyword.lower() in title.lower():
                    found_count += 1
                    result_html += f"""
                    <div style="border-bottom: 1px solid #ccc; margin-bottom: 10px;">
                        <p><b>編號：</b> {found_count}</p>
                        <p><b>片名：</b> {title}</p>
                        <p><b>上映日期：</b> {movie.get('showDate', '未知')}</p>
                        <p><a href="{movie.get('hyperlink', '#')}" target="_blank">點我查看電影介紹</a></p>
                        <img src="{movie.get('picture', '')}" width="150" alt="電影海報"><br><br>
                    </div>
                    """
            
            if found_count > 0:
                html_content += f"<h3>找到 {found_count} 部符合「{keyword}」的電影：</h3>" + result_html
            else:
                html_content += f"<p style='color:red;'>抱歉，資料庫中找不到包含「{keyword}」的電影。</p>"
        else:
            html_content += "<p>請輸入片名關鍵字。</p>"

    html_content += "<br><a href='/'>返回首頁</a>"
    return html_content


@app.route("/spidermovie")
def spidermovie():
    R = ""

    db = firestore.client()

    import requests
    from bs4 import BeautifulSoup
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"

    sp = BeautifulSoup(Data.text, "html.parser")
    lastUpdate = sp.find(class_="smaller09").text.replace("更新時間；","")

    result=sp.select(".filmListAllX li")

    total = 0

    for item in result:
      movie_id = item.find("a").get("href").replace("/movie/","").replace("/","")
      title = item.find("div", class_="filmtitle").text
      picture = "http://www.atmovies.com.tw" + item.find("img").get("src")
      hyperlink = "http://www.atmovies.com.tw" + item.find("a").get("href")

      showDate = item.find(class_="runtime").text[5:15]

      total += 1

      doc = {
          "title": title,
          "picture": picture,
          "hyperlink": hyperlink,
          "showDate": showDate,
          "lastUpdate": lastUpdate
          #"showLength": showLength, 這個是片長的部分
      }

      doc_ref = db.collection("電影2B").document(movie_id)
      doc_ref.set(doc)

    R += "網站最近更新日期" + lastUpdate + "<br>"
    R += "總共爬取" + str(total) + "部電影到資料庫"
        
    return R

@app.route("/movie1")
def movie1():
    R = ""
    url = "https://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    #print(Data.text)
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".filmListAllX li")
    for item in result:
        name = item.find("img").get("alt")
        introduce = "https://www.atmovies.com.tw" + item.find("a").get("href")
        img_src = "https://www.atmovies.com.tw" + item.find("img").get("src")
        
        R += f"<a href='{introduce}'><h2>{name}</h2></a>"
        R += f"<img src='{img_src}' width='200'><br><br>"
        
    return R

@app.route("/spider")
def spider():
    R = ""
    url = "https://www1.pu.edu.tw/~tcyang/course.html"
    try:
        Data = requests.get(url)
        Data.encoding = "utf-8"
        sp = BeautifulSoup(Data.text, "html.parser")
        result = sp.select("td")
        for i in result:
            R += i.text + i.get("href") + "<br>"

    except Exception as e:
        R = f"爬蟲抓取失敗: {e}"
    return R

@app.route("/read")
def read():
    Result = "<h3>靜宜資管最新 5 筆資料：</h3>"
    db = firestore.client()
    # 專注讀取「靜宜資管」集合
    collection_ref = db.collection("靜宜資管") 
    docs = collection_ref.order_by("lab", direction=firestore.Query.DESCENDING).limit(5).get()    
    
    for doc in docs:
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/read1", methods=["GET", "POST"])
def read1():
    # 建立網頁基礎結構 (對應圖片中的標題與輸入框)
    html_content = """
    <h2 style="font-weight: bold;">靜宜資管老師查詢</h2>
    <form action="/read1" method="POST">
        <label>請輸入老師姓名關鍵字：</label>
        <input type="text" name="keyword">
        <button type="submit">查詢</button>
    </form>
    <hr>
    """
    
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        
        if keyword:
            db = firestore.client()
            collection_ref = db.collection("靜宜資管")
            docs = collection_ref.get()
            
            result_output = ""
            found = False
            
            # 顯示「查詢結果 (關鍵字: XXX):」
            html_content += f"<h3>查詢結果 (關鍵字: {keyword}):</h3>"
            
            for doc in docs:
                teacher = doc.to_dict()
                name = teacher.get("name", "")
                lab = teacher.get("lab", "尚未提供") # 假設欄位名稱為 lab
                
                # 關鍵字比對
                if keyword in name:
                    found = True
                    # 格式化輸出：[藍色老師姓名] 老師的研究是在 [研究室]
                    result_output += f"<p><b style='color:blue;'>{name}</b> 老師的研究是在 <b>{lab}</b></p>"
            
            if found:
                html_content += result_output
            else:
                html_content += f"<p style='color:red;'>抱歉，查無此關鍵字姓名之老師資料</p>"
        else:
            html_content += "<p>請輸入關鍵字進行查詢。</p>"
                
    # 返回首頁連結 (對應圖片中的紫色連結)
    html_content += "<br><a href='/' style='color:purple; text-decoration:none;'>返回首頁</a>"
    
    return html_content

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime=str(now))

@app.route("/me")
def me():
    return render_template("about.html")

@app.route("/welcome", methods=["GET"])
def welcome():
    user = request.values.get("u")
    d = request.values.get("d")
    return render_template("welcome.html", name=user, d=d)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form.get("user", "未知")
        pwd = request.form.get("pwd", "未知")
        result = f"您輸入的帳號是：{user} ; 密碼為：{pwd}"
        return result
    else:
        return render_template("account.html")

@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        try:
            base_num = float(request.form.get("base_num", 0))
            exp_val = float(request.form.get("exp_val", 0))
            power_result = math.pow(base_num, exp_val)
            
            root_degree = float(request.form.get("root_degree", 1))
            if root_degree == 0:
                root_result = "次根數不可為 0"
            elif base_num < 0 and root_degree % 2 == 0:
                root_result = "負數無法開偶數次方根"
            else:
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