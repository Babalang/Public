from flask import Flask,session, render_template, redirect,url_for,request
from flask_socketio import SocketIO
from flask_socketio import emit
from datetime import timedelta
import string
from random import *
import json
import os
from cryptography.fernet import Fernet
from flask_login import LoginManager,UserMixin,login_user,current_user,login_required,logout_user
from werkzeug.security import generate_password_hash,check_password_hash

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
login_manager.init_app(app)

@app.before_request
def before_request():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=20)
	session.modified = True

@login_manager.user_loader
def load_user(user_id):
	users = json_variable("comptes")
	return User(user_id, users[user_id]) if user_id in users.keys() else None

class User(UserMixin):
	def __init__(self, id, password):
		self.id = id
		self.password = password
	def get_id(self):
		return self.id
	
	def get_password(self):
		return self.password
	
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

def createMDP():
	length = 50
	caracteres = string.ascii_letters + string.digits
	return "".join(choice(caracteres) for _ in range(length))

def json_save(files, items):
	with open(files, 'w') as file:
		json.dump(items, file)

def json_create(files, items):
	if not os.path.exists(f'data/{files}.json'):
		with open(f'data/{files}.json','w') as f:
			json.dump(items, f)

# Permet de rÃ©cupÃ©rer un fichier json
def json_load(files):
	with open(files) as file:
		return json.load(file)

# Permet de rÃ©cupÃ©rer une variable dans un fichier json
def json_variable(files):
	return json_load(f"data/{files}.json")
	
def json_sendVariable(files, element):
	json_save(f"data/{files}.json", element)

# Chiffrer un mot de passe
def encrypt(mot_de_passe,key):
	fernet = Fernet(key)
	return fernet.encrypt(mot_de_passe.encode())

# Décrypter un mot de passe
def decrypt(mot_de_passe_chiffre,key):
	fernet = Fernet(key)
	return fernet.decrypt(mot_de_passe_chiffre.encode()).decode()
	

@socketio.on('Get_a_password')
def Get_a_password():
	emit("Get_a_password",{"mdp" : createMDP()})

@socketio.on("Saving_a_password")
def Saving_a_password(data):
	if current_user.is_authenticated:
		libelle = data["libelle"]
		MotDP = data["MDP"]
		chiffrement = json_variable(f"{current_user.get_id()}_chiffrement")
		MotDePasse = json_variable(f"{current_user.get_id()}_MotDePasse")
		key = Fernet.generate_key()
		MotDePasse[libelle] = encrypt(MotDP,key).decode("UTF-8")
		chiffrement[libelle] = key.decode("UTF-8")
		json_sendVariable(f"{current_user.get_id()}_MotDePasse",MotDePasse)
		json_sendVariable(f"{current_user.get_id()}_chiffrement",chiffrement)
		key = None
		emit("Saved")
	else :
		emit("error", {"erreur": "Vous n'êtes pas connecté"})

@socketio.on("Getting_a_password")
@login_required
def Getting_a_password(data):
	libelle = data["libelle"]
	MDP_user = data["MDP"]
	if (check_password_hash(current_user.get_password(), MDP_user)) and (libelle in json_variable(f"{current_user.get_id()}_MotDePasse").keys()):
		chiffrement = json_variable(f"{current_user.get_id()}_chiffrement")[libelle]
		MotDePass = json_variable(f"{current_user.get_id()}_MotDePasse")[libelle]
		emit("Get",{"MDP":decrypt(MotDePass,chiffrement)})
	else : emit("error",{"erreur":"Libellé ou mot de passe incorrect"})

@socketio.on("Deleting_a_password")
@login_required
def Deleting_a_password(data):
	libelle = data["libelle"]
	MDP_user = data["MDP"]
	if (check_password_hash(current_user.get_password(), MDP_user)) and (libelle in json_variable(f"{current_user.get_id()}_MotDePasse").keys()):
		chiffrement = json_variable(f"{current_user.get_id()}_chiffrement")
		MotDePass = json_variable(f"{current_user.get_id()}_MotDePasse")
		chiffrement.pop(libelle)
		MotDePass.pop(libelle)
		json_sendVariable(f"{current_user.get_id()}_MotDePasse",MotDePass)
		json_sendVariable(f"{current_user.get_id()}_chiffrement",chiffrement)
		emit("Deleted")
	else : emit("error",{"erreur":"Libellé ou mot de passe incorrect"})

@app.route('/login', methods=['GET', 'POST'])
def login():
	logout_user()
	if request.method == 'POST':
		# Vérification de l'identité de l'utilisateur
		user_id = request.form['user_id']
		user_password = request.form['user_password']
		user = load_user(user_id)
		if (user is not None) and (check_password_hash(user.password, user_password)):
			user = User(user_id,user_password)
			login_user(user)
			return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def submit_register():
	logout_user()
	if request.method == 'POST':
		# Vérification de l'identité de l'utilisateur
		user_id = request.form['user_id']
		user_password = request.form['user_password']
		user = load_user(user_id)
		if (user is None):
			json_create(f"{user_id}_chiffrement",{})
			json_create(f"{user_id}_MotDePasse",{})
			temp_user = json_variable("comptes")
			temp_user[user_id] = generate_password_hash(user_password)
			json_sendVariable("comptes", temp_user)
			user = User(user_id,user_password)
			login_user(user)
			return redirect(url_for('index'))
	return render_template('register.html')

@app.route("/")
def index():
	return render_template("index.html",id=current_user.get_id())

@app.route('/protected')
@login_required
def protected():
	return 'This page is protected. Only authenticated users can see it.'

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/Generate_password')
def Generate_password():
	return render_template("Generate_password.html")

@app.route('/Del_password')
@login_required
def Del_password():
	return render_template("Del_password.html")

@app.route('/Display')
@login_required
def Display_password():
	return render_template("Display_password.html")

@app.route("/DelAccount")
@login_required
def DelAccount():
	temp_compte = json_variable("comptes")
	temp_compte.pop(current_user.get_id())
	json_sendVariable("comptes",temp_compte)
	os.remove(f'data/{current_user.get_id()}_chiffrement.json')
	os.remove(f'data/{current_user.get_id()}_MotDePasse.json')
	return redirect(url_for('logout'))


if __name__ == '__main__':
	socketio.run(app, port=5224)