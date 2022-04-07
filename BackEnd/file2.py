from flask import Flask, request, jsonify, make_response, request, render_template, session, flash
import jwt
from datetime import datetime, timedelta
from functools import wraps


app=Flask(__name__,template_folder='Templates')


app.config['SECRET_KEY'] = 'ieB-yviFMH_EevsJ'



def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'The Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return 'logged in currently'



@app.route('/public')
def public():
    return 'For Public'



@app.route('/auth')
@token_required
def auth():
    return 'The JWT is verified. Welcome to your dashboard !  '

# Login page for the route


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True

        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})



@app.route('/logout', methods=['POST'])
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)