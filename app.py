######################################
# author ben lawson <balawson@bu.edu>
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
import requests, json, unicodedata

#for image uploading
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = "hidden"  # Change this!


#new login
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

#end login
#begin code used for login
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()
# cursor.execute("SELECT email from Users")
# users = cursor.fetchall()

# def getUserList():
# 	cursor = conn.cursor()
# 	cursor.execute("SELECT email from Users")
# 	return cursor.fetchall()

# class User(flask_login.UserMixin):
# 	pass

# @login_manager.user_loader
# def user_loader(email):
# 	users = getUserList()
# 	if not(email) or email not in str(users):
# 		return
# 	user = User()
# 	user.id = email
# 	return user

# @login_manager.request_loader
# def request_loader(request):
# 	users = getUserList()
# 	email = request.form.get('email')
# 	if not(email) or email not in str(users):
# 		return
# 	user = User()
# 	user.id = email
# 	cursor = mysql.connect().cursor()
# 	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
# 	data = cursor.fetchall()
# 	pwd = str(data[0][0] )
# 	user.is_authenticated = request.form['password'] == pwd
# 	return user

# '''
# A new page looks like this:
# @app.route('new_page_name')
# def new_page_function():
# 	return new_page_html
# '''

# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	if flask.request.method == 'GET':
# 		return '''
# 			   <form action='login' method='POST'>
# 				<input type='text' name='email' id='email' placeholder='email'></input>
# 				<input type='password' name='password' id='password' placeholder='password'></input>
# 				<input type='submit' name='submit'></input>
# 			   </form></br>
# 		   <a href='/'>Home</a>
# 			   '''
# 	#The request method is POST (page is recieving data)
# 	email = flask.request.form['email']
# 	cursor = conn.cursor()
# 	#check if email is registered
# 	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
# 		data = cursor.fetchall()
# 		pwd = str(data[0][0] )
# 		if flask.request.form['password'] == pwd:
# 			user = User()
# 			user.id = email
# 			flask_login.login_user(user) #okay login in user
# 			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file

# 	#information did not match
# 	return "<a href='/login'>Try again</a>\
# 			</br><a href='/register'>or make an account</a>"

# @app.route('/logout')
# def logout():
# 	flask_login.logout_user()
# 	return render_template('hello.html', message='Logged out')

# @login_manager.unauthorized_handler
# def unauthorized_handler():
# 	return render_template('index.html')

# #you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
# @app.route("/register", methods=['GET'])
# def register():
# 	return render_template('register.html', supress='True')

# @app.route("/register", methods=['POST'])
# def register_user():
# 	try:
# 		email=request.form.get('email')
# 		password=request.form.get('password')
# 	except:
# 		print("couldn't find all tokens") #this prints to shell, end users will not see this (all print statements go to shell)
# 		return flask.redirect(flask.url_for('register'))
# 	cursor = conn.cursor()
# 	test =  isEmailUnique(email)
# 	if test:
# 		print(cursor.execute("INSERT INTO Users (email, password) VALUES ('{0}', '{1}')".format(email, password)))
# 		conn.commit()
# 		#log user in
# 		user = User()
# 		user.id = email
# 		flask_login.login_user(user)
# 		return render_template('hello.html', name=email, message='Account Created!')
# 	else:
# 		print("couldn't find all tokens")
# 		return flask.redirect(flask.url_for('register'))

# def getUsersPhotos(uid):
# 	cursor = conn.cursor()
# 	cursor.execute("SELECT imgdata, picture_id, caption FROM Pictures WHERE user_id = '{0}'".format(uid))
# 	return cursor.fetchall() #NOTE return a list of tuples, [(imgdata, pid, caption), ...]

# def getUserIdFromEmail(email):
# 	cursor = conn.cursor()
# 	cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
# 	return cursor.fetchone()[0]

# def isEmailUnique(email):
# 	#use this to check if a email has already been registered
# 	cursor = conn.cursor()
# 	if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
# 		#this means there are greater than zero entries with that email
# 		return False
# 	else:
# 		return True
#end login code

@app.route('/profile')
@flask_login.login_required
def protected():
	return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile")

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		caption = request.form.get('caption')
		photo_data =imgfile.read()
		cursor = conn.cursor()
		cursor.execute('''INSERT INTO Pictures (imgdata, user_id, caption) VALUES (%s, %s, %s )''', (photo_data, uid, caption))
		conn.commit()
		return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!', photos=getUsersPhotos(uid), base64=base64)
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		return render_template('upload.html')
#end photo uploading code






url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "07f5ddb891msh21c512d703b7bd5p1cb69cjsnc2ae67f8953b",
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

find = "recipes/findByIngredients"
randomFind = "recipes/random"
	

@app.route('/recipes')
def get_recipes():
	if (str(request.args['ingridients']).strip() != ""):
		# If there is a list of ingridients -> list
		querystring = {"number":5,"ranking":"1","ignorePantry":"false","ingredients":request.args['ingridients']}
		response = requests.request("GET", url + find, headers=headers, params=querystring).json()
		return render_template('recipes.html', recipes=response)
	else:
		# Random recipes
		querystring = {"number":"5"}
		response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()
		print(response)
		return render_template('recipes.html', recipes=response['recipes'])




#default page
@app.route("/", methods=['GET'])
def hello():
	return render_template('home.html')

@app.route("/left.html", methods=['GET'])
# @flask_login.login_required
def new_page_function():
	return render_template('left.html')

@app.route("/carousel.html", methods=['GET'])
def carousel():
	return render_template('carousel.html')

# @app.route("/home.html", methods=['GET'])
# def home():
# 	return render_template('home.html')

if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=5000, debug=True, threaded=True)

