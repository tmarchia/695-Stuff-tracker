from logging import error
from flask import Flask,render_template,session,request
import sqlite3
from flask.helpers import url_for

from werkzeug.utils import redirect
app=Flask(__name__,template_folder='Templates')
app.secret_key = "mykey"

@app.route("/" ,methods =['GET','POST'])
def welcome():
    msg = None
    if (request.method == 'POST'):
        if (request.form ['username'] != "" and request.form['password']!= ""):
            username = request.form["username"]
            password = request.form["password"]
            conn =sqlite3.connect("signup.db")
            c = conn.cursor()
            c.execute("INSERT INTO person VALUES('"+username+"','"+password+"')")
            msg = "Your account is created"
            conn.commit()
            conn.close()
        else:
            msg ="Something went wrong"
    
    return render_template("signup.html" , msg = msg)
@app.route("/login" ,methods =['GET','POST'])
def login():
    r = ""
    msg = ""
    # session.pop('logged_in' ,None)
    if(request.method == "POST"):
        username =request.form["username"]
        password =request.form["password"]
        conn =sqlite3.connect("signup.db")
        c = conn.cursor()
        c.execute("SELECT * FROM person WHERE username = '"+username+"'and password = '"+password+"'")
        r = c.fetchall()
        for i in r:
            if (username ==i[0] and password ==i[1]):
                session["loggedin"] = True
                session["username"] = username
                return redirect(url_for("about"))
            else:
                msg= "Please enter valid username and password"
                
    return render_template("login.html",msg = msg)

if __name__ =="__main__":
    app.run(debug=True)
