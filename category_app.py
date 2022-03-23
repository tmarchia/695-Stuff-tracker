"""
This Script is to implement our flask methods to connect to our front end
"""

from flask import Flask, request, render_template, redirect
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
        categoryDb.create_category(user_name, category, location)
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
        itemDb.add_item(user_name, item_name, category,
                        location, purchase_date, tags)
        # TODO - comment this in when home page is available
        return redirect('/home_page')
    elif request.method == 'GET':
        categories = categoryDb.get_categories(user_name)
        return render_template('AddItem.html', categories=categories)


@app.route('/home_page', methods=('GET', 'POST'))
def home_page():
    return render_template("HomePage.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
