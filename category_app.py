"""
This Script is to implement our flask methods to connect to our front end
"""
import os
import shutil

import requests
import jsons
import boto3

from flask import Flask, request, render_template, redirect, session, url_for
from BackEnd import CategoryDatabase, ItemDatabase

app = Flask(__name__)

# Access secret key needed for session
key_file_path = '/home/ec2-user/config/SecretSessionKey.txt'
if os.path.exists(key_file_path):
    with open(key_file_path) as key_file:
        lines = key_file.readlines()
        secret_key = lines[0]
app.secret_key = secret_key

# Access AWS keys needed to access AWS services
fixer_key_file_path = '/home/ec2-user/config/FixerKeys.txt'
if os.path.exists(fixer_key_file_path):
    with open(fixer_key_file_path) as key_file:
        lines = key_file.readlines()
        access_key_id = lines[0].split(':')[1].strip()
        secret_access_key = lines[1].split(':')[1].strip()

BUCKET_NAME = 'stevensfixerappimages'

# Setup connections to dynamoDb and S3
categoryDb = CategoryDatabase.CategoryDatabase()
itemDb = ItemDatabase.ItemDatabase()
s3 = boto3.client('s3',
                  aws_access_key_id=access_key_id,
                  aws_secret_access_key=secret_access_key,
                  region_name='us-east-1')


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

            # If image was added store in S3
            filename = ""
            item_filename = ""
            if 'img' in request.files and request.files['img'].filename != '':
                # Image found
                img = request.files['img']
                filename = img.filename
                item_filename = item_name + '.jpg'  # Name used for stored image
                key = '/static/' + \
                    session.get('username') + '/' + item_name + '.jpg'

                img.save(filename)
                s3.upload_file(
                    Bucket=BUCKET_NAME,
                    Filename=filename,
                    Key=key
                )
                curr_dir = os.getcwd()
                os.remove(curr_dir + '/' + filename)

                print("Upload Done ! " + key)
            else:
                print("No image")

            category = request.form['Select Category']
            location = request.form['location']
            purchase_date = request.form['purchase_date']
            tags = request.form['tags']

            itemDb.add_item(session['username'], item_name,
                            item_filename, category, location, purchase_date, tags)

            return redirect('/home_page')

        # Pass users current categories to be used as options when adding item
        categories = categoryDb.get_categories(session['username'])

        return render_template('AddItem.html', categories=categories)

    return redirect('/signout')


@app.route('/update_item/<item_name>', methods=('GET', 'POST'))
def update_item(item_name):
    """ Function for the update item webpage """
    if session.get('username'):
        if request.method == 'POST':
            item_name = request.form['item_name']

            # If image was added store in S3
            filename = ""
            item_filename = ""
            if 'img' in request.files and request.files['img'].filename != '':
                # Image found
                img = request.files['img']
                filename = img.filename
                item_filename = item_name + '.jpg'  # Name used for stored image
                key = '/static/' + \
                    session.get('username') + '/' + item_filename

                img.save(filename)
                s3.upload_file(
                    Bucket=BUCKET_NAME,
                    Filename=filename,
                    Key=key
                )
                curr_dir = os.getcwd()
                os.remove(curr_dir + '/' + filename)

                print("Upload Done ! " + key)
            else:
                # If image not added on update keep previous image_name key/item
                item = itemDb.get_item_by_name(session['username'], item_name)
                item_filename = item[0]["imageName"]
                print("No new image")

            category = request.form['Select Category']
            location = request.form['location']
            purchase_date = request.form['purchase_date']
            tags = request.form['tags']

            itemDb.add_item(session['username'], item_name,
                            item_filename, category, location, purchase_date, tags)

            return redirect('/home_page')

        # Populate update page with current item values
        item = itemDb.get_item_by_name(session['username'], item_name)
        categories = categoryDb.get_categories(session['username'])

        return render_template('UpdateItem.html', categories=categories, item=item[0])

    return redirect('/signout')


@app.route('/delete_item/<item_name>', methods=('GET', 'POST'))
def delete_item(item_name):
    """ Function for the deleting an item """
    if session.get('username'):
        itemDb.delete_item(session['username'], item_name)
        return redirect(url_for("home_page"))

    return redirect('/signout')


@app.route('/all_items', methods=('GET', 'POST'))
def all_items():
    """ Function for listing all items """
    if session.get('username'):
        items = itemDb.get_all_items(session['username'])
        return render_template("All_Items.html", items=items)

    return redirect('/signout')


def images(filename):
    """ Method used to retrieve item and item location """
    url = ''
    if filename != "":
        path = '/static/' + session.get('username') + '/'
        url = path + filename
        try:
            # Try to get file from S3 and move to static folder for user
            s3.download_file(BUCKET_NAME, url, filename)

            curr_dir = os.getcwd()
            current = curr_dir + "/" + filename
            move_to = curr_dir + url
            if not os.path.exists(curr_dir + path):
                os.makedirs(curr_dir + path)

            shutil.move(current, move_to)
        except:
            print("Image " + url + " not found in S3")
    return url


@app.route('/single_item/<item_name>', methods=('GET', 'POST'))
def single_item(item_name):
    """ Function for displaying a single items """
    if session.get('username'):
        item = itemDb.get_item_by_name(session['username'], item_name)

        # Get related items to list below single item
        related_items = itemDb.get_items_by_category(
            session['username'], item[0]['category'])

        return render_template("Single_Item.html", item=item[0], related_items=related_items)

    return redirect('/signout')


@app.route('/search_items/<search_word>', methods=('GET', 'POST'))
def search_items(search_word):
    """ Function for search items """
    if session.get('username'):
        items = itemDb.search_items(
            session['username'], search_word.lower())
        return render_template("search.html", items=items)

    return redirect('/signout')


@app.route('/search_items', methods=('GET', 'POST'))
def search_items():
    """ Function for empty search """
    return redirect('/home_page')


@app.route('/home_page/', methods=('GET', 'POST'))
def home_page():
    """ Function for rendering homepage """
    if not session.get('username'):
        code = request.args.get('code')
        session['username'] = get_user_name(code)

    if request.method == 'GET':
        items = itemDb.get_all_items(session['username'])
        return render_template("index.html", username=session['username'], items=items)

    elif request.method == 'POST':
        search_word = request.form['search_word']
        return redirect(url_for('search_items', search_word=search_word))


@app.route('/signout', methods=('GET', 'POST'))
def signout():
    """ Function for signing out """
    if session.get('username'):
        session.pop('username')
    return redirect("http://www.stevensfixerapp.com")


def get_user_name(code):
    """ Using access token retrieve user name """
    # Get access token
    url = 'https://fixerapp.auth.us-east-1.amazoncognito.com/oauth2/token'
    headers = {'Accept-Encoding': 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code,
            'redirect_uri': 'https://app.stevensfixerapp.com:5000/home_page/', 'client_id': '2ugh0ft9kuhn66qqhlvb7952f4'}

    res = requests.post(url, data=data, headers=headers)
    access_token = jsons.loads(res.text)['access_token']

    # Get user name
    url = 'https://fixerapp.auth.us-east-1.amazoncognito.com/oauth2/userInfo'
    headers = {'Authorization': 'Bearer '+access_token}
    data = {}

    res = requests.get(url, data=data, headers=headers)
    username = jsons.loads(res.text)['username']

    return username


if __name__ == "__main__":
    app.jinja_env.globals.update(images=images)
    app.run(host="0.0.0.0", port=5000, ssl_context=(
        'fullchain.pem', 'privkey.pem'))
