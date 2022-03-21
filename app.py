from logging import error
from flask import Flask,render_template,session,request
app=Flask(__name__,template_folder='Templates')
app.secret_key = "mykey"


@app.route("/" ,methods =['GET','POST'])
def welcome():
    error = None
    if request.method == 'POST':
        if request.form ['username'] != 'kunal' or request.form['password']!= 'kunal@123':
            error = "Please insert valid details"
        else:
            session['logged_in']= True
            return render_template("about.html")
    return render_template("index.html" , error = error)


@app.route("/about")
def about ():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop('logged_in' ,None)
    return render_template("index.html")

if __name__ =="__main__":
    app.run(debug=True)
