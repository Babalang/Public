from flask import Flask,session, render_template, redirect,url_for,request,flash,send_file
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from datetime import timedelta
from random import *
import json
import logging
import os
from flask_login import LoginManager,UserMixin,login_user,current_user,login_required,logout_user
from passlib.hash import bcrypt

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.permanent_session_lifetime = timedelta(minutes=20)
socketio = SocketIO(app)
login_manager.init_app(app)
# Dossier de destination pour les fichiers téléchargés
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/upload', methods=['POST'])
def upload_file():
	if 'file' not in request.files:
		return redirect(request.url)
	uploaded_files = request.files.getlist('file')
	for file in uploaded_files:
		print(file)
		if file.filename:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	flash('Opération réussie!', 'success')
	app.logger.info(f"Un dossier/fichier est enregitré par {current_user.get_id()}")
	return redirect(url_for('index'))
	
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
	

@app.route('/login', methods=['POST'])
def login():
	logout_user()
	if request.method == 'POST':
		# Vérification de l'identité de l'utilisateur
		user_id = request.form['user_id']
		user_password = request.form['user_password']
		user = load_user(user_id)
		if (user is not None) and (bcrypt.verify(user_password, user.password)):
			user = User(user_id,user_password)
			login_user(user)
			app.logger.info(f"L'utilisateur : {current_user.get_id()} se connecte")
			return redirect(url_for('index'))
		else:
			app.logger.warning("Tentative de connexion échouée")
			return render_template('login.html')
	else:
		app.logger.warning("Tentative de connexion échouée")
		return render_template('login.html')

@app.route('/login',methods=['GET'])
def affichelogin():
	app.logger.info("Un utilisateur va se connecter")
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
			temp_user = json_variable("comptes")
			temp_user[user_id] = bcrypt.using(rounds=12).hash(user_password)
			json_sendVariable("comptes", temp_user)
			user = User(user_id,user_password)
			login_user(user)
			app.logger.info(f"{user_id} est un nouveau membre")
			return redirect(url_for('index'))
	return render_template('register.html')

@app.route("/")
def index():
	app.logger.info(f"{current_user.get_id()} est dans le menu")
	return render_template("index.html",id=current_user.get_id())

@app.route('/protected')
@login_required
def protected():
	return 'This page is protected. Only authenticated users can see it.'

@app.route('/logout')
def logout():
	app.logger.info(f"{current_user.get_id()} se déconnecte")
	logout_user()
	return redirect(url_for('index'))

@app.route("/DelAccount")
@login_required
def DelAccount():
	temp_compte = json_variable("comptes")
	temp_compte.pop(current_user.get_id())
	json_sendVariable("comptes",temp_compte)
	app.logger.warning(f"{current_user.get_id()} Supprime son compte")
	return redirect(url_for('logout'))


@app.route('/liste_fichiers')
def liste_fichiers():
	fichiers = os.listdir(app.config['UPLOAD_FOLDER'])
	return '\n'.join(fichiers)

@app.route('/Telechargement')
def telechargement():
	fichiers = [fichier for fichier in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], fichier))]
	print(fichiers)
	app.logger.info(f"{current_user.get_id()}: Regarde les fichiers")
	return render_template("telechargement.html",fichiers=fichiers)

@app.route('/Telechargement/<nomfichier>')
def telecharger(nomfichier):
	chemin_complet = os.path.join(app.config['UPLOAD_FOLDER'], nomfichier)
	try:
		app.logger.info(f"{current_user.get_id()}: Télécharge : {chemin_complet}")
		# Utilisation de send_file pour envoyer le fichier au client en tant que pièce jointe
		return send_file(chemin_complet, as_attachment=True)
	except Exception as e:
		        # Gérer les erreurs de téléchargement ici
		flash(f"Erreur lors du téléchargement du fichier :{e}", 'fail')
		app.logger.error("Erreur lors du téléchargement")
		return redirect(url_for('telechargement'))  # Assurez-vous d'avoir la liste des fichiers à envoyer à la page

if __name__ == '__main__':
	host = '192.168.1.22'
	port = 5224
	print(f"Serveur Flask en cours d'écoute sur http://{host}:{port}/ Vos id de connexion sont : id = Admin MDP = AdminisSoCool@")
	app.logger.info(f"Le serveur se lance sur l'adresse : http://{host}:{port}/")
	app.run(host, port)
	