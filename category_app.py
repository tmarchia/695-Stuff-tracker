"""
This Script is to implement our flask methods to connect to our front end
"""

from flask import Flask, request, render_template, redirect, session
from BackEnd import CategoryDatabase, ItemDatabase

app = Flask(__name__)
categoryDb = CategoryDatabase.CategoryDatabase()
itemDb = ItemDatabase.ItemDatabase()
user_name = "test"  # TODO - figure out how to get user name


@app.route('/create_category', methods=('GET', 'POST'))
def create_new_category():
    """ Function for the create new category webpage """
    if request.method == 'POST':
        category = request.form['AddArea']
        location = request.form['location']
        categoryDb.create_category(session["username"], category, location)
        # TODO - comment this in when home page is available
        return redirect('/home_page')
    return render_template('AddCategory.html')


@app.route('/create_item', methods=('GET', 'POST'))
def create_new_item():
    """ Function for the create new category webpage """
    if request.method == 'POST':
        item_name = request.form['item_name']
        category = request.form['Select Category']
        location = request.form['location']
        purchase_date = request.form['purchase_date']
        tags = request.form['tags']
        itemDb.add_item(session["username"], item_name, category,
                        location, purchase_date, tags)
        # TODO - comment this in when home page is available
        return redirect('/home_page')
    elif request.method == 'GET':
        categories = categoryDb.get_categories(user_name)
        return render_template('AddItem.html', categories=categories)


@app.route("/", methods=['GET', 'POST'])
def welcome():
    msg = None
    if (request.method == 'POST'):
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
    r = ""
    msg = ""
    # session.pop('logged_in' ,None)
    if(request.method == "POST"):
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

    return render_template("Sign-in.html", msg=msg)


@app.route('/home_page', methods=('GET', 'POST'))
def home_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
