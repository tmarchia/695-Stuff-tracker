"""
This Script is to implement our flask methods to connect to our front end
"""
import os
from flask import Flask, request, render_template, redirect, session, url_for
from BackEnd import CategoryDatabase, ItemDatabase

app = Flask(__name__)
key_file_path = '/home/ec2-user/config/SecretSessionKey.txt'
if os.path.exists(key_file_path):
    with open(key_file_path) as key_file:
        lines = key_file.readlines()
        secret_key = lines[0]
app.secret_key = secret_key

categoryDb = CategoryDatabase.CategoryDatabase()
itemDb = ItemDatabase.ItemDatabase()


@app.route('/create_category', methods=('GET', 'POST'))
def create_new_category():
    """ Function for the create new category webpage """
    if session.get('username'):
        if request.method == 'POST':
            category = request.form['AddArea']
            location = request.form['location']
            categoryDb.create_category(session['username'], category, location)
            return redirect('/home_page')

        return render_template('AddCategory.html')

    return redirect('/signout')


@app.route('/create_item', methods=('GET', 'POST'))
def create_new_item():
    """ Function for the create new item webpage """
    if session.get('username'):
        if request.method == 'POST':
            item_name = request.form['item_name']
            category = request.form['Select Category']
            location = request.form['location']
            purchase_date = request.form['purchase_date']
            tags = request.form['tags']
            itemDb.add_item(session['username'], item_name, category,
                            location, purchase_date, tags)
            return redirect('/home_page')

        categories = categoryDb.get_categories(session['username'])
        return render_template('AddItem.html', categories=categories)

    return redirect('/signout')


@app.route('/delete_item', methods=('GET', 'POST'))
def delete_item():
    """ Function for the create new category webpage """
    if session.get('username'):
        item_name = request.form['item_name']
        itemDb.delete_item(session['username'], item_name)

        return redirect(url_for("home_page"))

    return redirect('/signout')


@app.route("/signup", methods=['GET', 'POST'])
def welcome():
    """ Function for sign up """
    msg = None
    if request.method == 'POST':
        if (request.form['username'] != "" and request.form['password'] != ""):
            username = request.form["username"]
            password = request.form["password"]
            conn = sqlite3.connect("signup.db")
            c = conn.cursor()
            c.execute("INSERT INTO person VALUES('"+username+"','"+password+"')")
            msg = "Your account is created"
            conn.commit()
            conn.close()
        else:
            msg = "Something went wrong"

    return render_template("Sign-up.html", msg=msg)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Function for log up """
    r = ""
    msg = ""
    # session.pop('logged_in' ,None)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("signup.db")
        c = conn.cursor()
        c.execute("SELECT * FROM person WHERE username = '" +
                  username+"'and password = '"+password+"'")
        r = c.fetchall()
        for i in r:
            if (username == i[0] and password == i[1]):
                session["loggedin"] = True
                session["username"] = username
                return redirect(url_for("about"))
            else:
                msg = "Please enter valid username and password"

    return render_template("Sign-In.html", msg=msg)


@app.route('/all_items', methods=('GET', 'POST'))
def all_items():
    """ Function for listing all items """
    if session.get('username'):
        return render_template("All_Items.html")

    return redirect('/signout')


@app.route('/home_page/', methods=('GET', 'POST'))
def home_page():
    """ Function for rendering homepage """
    if session.get('username'):
        session['username'] = "test"

        return render_template("index.html")

    return redirect('/signout')


@app.route('/signout', methods=('GET', 'POST'))
def signout():
    """ Function for signing out """
    if session.get('username'):
        session.pop('username')

    return redirect("www.stevensfixerapp.com")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context='adhoc')
