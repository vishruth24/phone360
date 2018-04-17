from flask import Flask, render_template, request,url_for,redirect,flash
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

@app.route('/brand',methods=['POST','GET'])
def phone():
    if request.method == "POST":
        pass
    else:
        conn=sql.connect("static/phone.db")
        c=conn.cursor()
        c.execute('SELECT distinct(brand) FROM phones')
        brand = c.fetchall()
        c.close
        conn.close()
        return render_template('brands.html',brand=brand)

@app.route('/brand/<brand_name>')
def gen(brand_name):
    conn=sql.connect("static/phone.db")
    c=conn.cursor()
    c.execute('SELECT img_url,model FROM phones where brand=(?)',[brand_name])
    images = c.fetchall()
    c.close
    conn.close()
    return render_template("phones.html",image=images,name=brand_name)

@app.route('/brand/<brand_name>/<pname>')
def details(brand_name,pname):
    conn=sql.connect("static/phone.db")
    c=conn.cursor()
    c.execute('SELECT * FROM phones where brand=(?) and model=(?)',[brand_name,pname])
    stuff = c.fetchall()
    c.close
    conn.close()

    return render_template('detials.html',name=pname,data=stuff)

@app.route('/compare/<m1>/<m2>')
def compare(m1,m2):
    conn=sql.connect("static/phone.db")
    c=conn.cursor()
    c.execute('SELECT * FROM phones where model=(?)',[m1])
    model1 = c.fetchall()
    c.execute('SELECT * FROM phones where model=(?)',[m2])
    model2 = c.fetchall()

    c.close
    conn.close()

    return render_template('compare.html',data1=model1,data2=model2)

@app.route('/compare',methods=["post",'GET'])
def comp():

    if request.method == "POST":
        b1=request.form['comp1']
        b2=request.form['comp2']
        conn=sql.connect("static/phone.db")
        c=conn.cursor()
        c.execute('SELECT model FROM phones where brand=(?)',[b1])
        m1 = c.fetchall()
        c.execute('SELECT model FROM phones where brand=(?)',[b2])
        m2 = c.fetchall()

        c.close
        conn.close()
        return render_template("bphone.html",m1=m1,m2=m2)


    else:
        conn=sql.connect("static/phone.db")
        c=conn.cursor()
        c.execute('SELECT distinct(brand) FROM phones')
        brand = c.fetchall()
        c.close
        conn.close()
        return render_template('comp.html',data=brand)

@app.route('/insert',methods=["POST","GET"])
def insert():
    if request.method == "POST":
        conn=sql.connect("static/phone.db")
        c=conn.cursor()
        brand1=request.form['brand']
        Model=request.form['Model']
        Network=request.form['Network']
        Dimension=request.form['Dimension']
        Announced=request.form['Announced']
        SIM=request.form['SIM']
        Type=request.form['Type']
        Resolution=request.form['Resolution']
        OS=request.form['OS']
        CPU=request.form['CPU']
        GPU=request.form['GPU']
        RAM=request.form['RAM']
        Camera=request.form['Camera']
        Battery=request.form['Battery']
        Price=request.form['Price']
        image=request.form['image']
        Price=str(int(Price)/80)
        c.execute('INSERT into phones (brand,model,network_technology,announced,dimentions,SIM,display_type,display_resolution,OS,CPU,GPU,RAM,\
        primary_camera,battery,approx_price_EUR,img_url) values ((?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),(?),\
        (?))',[brand1,Model,Network,Dimension,Announced,SIM,Type,Resolution,OS,CPU,GPU,RAM,Camera,Battery,Price,image])
        conn.commit()
        c.close
        flash("Phone inserted successfully")
        conn.close()
        return render_template('insert.html')
    if request.method=="GET":
        return render_template('insert.html')

@app.route('/useless',methods=["POST","GET"])
def useless():
    if request.method=="POST":
        m1=request.form['p1']
        m2=request.form['p2']

        return redirect("compare/{}/{}".format(m1,m2))
    else:
        return "Hi there! Hope youre having a great day"

@app.route('/filter',methods=["POST","GET"])
def filter():
    if request.method=="POST":
        comp=request.form["comp1"]
        cor=request.form["cores"]
        ram123=request.form["ram123"]
        # bat=request.form["bat"]
        conn=sql.connect("static/phone.db")
        c=conn.cursor()
        c.execute('SELECT img_url,model,brand FROM phones where brand = (?) and CPU like (?) and RAM \
        like (?)',[comp,"%"+cor+"%","%"+ram123+"%"])
        images = c.fetchall()
        c.close
        conn.close()
        return render_template("phones2.html",image=images)



    else:
        conn=sql.connect("static/phone.db")
        c=conn.cursor()
        c.execute('SELECT distinct(brand) FROM phones')
        brand = c.fetchall()
        c.close
        conn.close()
        return render_template('filter.html',data=brand)





app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
