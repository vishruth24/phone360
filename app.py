from flask import Flask, render_template, request,url_for,redirect
import sqlite3 as sql
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/iphonex')
def iphonex():
    return redirect("https://www.apple.com/in/iphone-x/")

@app.route('/samsung')
def samsung():
    return redirect("http://www.samsung.com/global/galaxy/galaxy-s9/")

@app.route('/brand/<brand_name>')
def gen(brand_name):
    conn=sql.connect("static/phone.db")
    c=conn.cursor()
    c.execute('SELECT img_url,model FROM phones where brand=(?)',[brand_name])
    images = c.fetchall()
    c.close
    conn.close()
    return render_template("generic.html",image=images,name=brand_name)

@app.route('/lol')
def lol():
    return render_template('generic.html')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
