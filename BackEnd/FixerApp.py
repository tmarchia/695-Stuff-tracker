"""
This Script is to implement our flask methods to connect to our front end
"""

import CategoryDatabase
from flask import Flask

app = Flask(__name__)
categoryDb = CategoryDatabase.CategoryDatabase()
user_name = "test"  # TODO - figure out how to get user name


@app.route('/create_category', methods=('GET', 'POST'))
def create_new_category():
    """ Function for the create new category webpage """
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        categoryDb.create_category(user_name, category, description)

    return render_template('home_page.html')


app.run()
