import os
import string
from random import *
import json
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash,check_password_hash

def createMDP():
	length = 50
	caracteres = string.ascii_letters + string.digits
	return "".join(choice(caracteres) for _ in range(length))

def json_save(files, items):
	with open(files, 'w') as file:
		json.dump(items, file)

def json_create(files, items):
	if not os.path.exists(f'{os.getcwd()}/app/data/{files}.json'):
		with open(f'{os.getcwd()}/app/data/{files}.json','w') as f:
			json.dump(items, f)

# Permet de rÃ©cupÃ©rer un fichier json
def json_load(files):
	with open(files) as file:
		return json.load(file)

# Permet de rÃ©cupÃ©rer une variable dans un fichier json
def json_variable(files):
	return json_load(f"{os.getcwd()}/app/data/{files}.json")
	
def json_sendVariable(files, element):
	json_save(f"{os.getcwd()}/app/data/{files}.json", element)

# Chiffrer un mot de passe
def encrypt(mot_de_passe,key):
	fernet = Fernet(key)
	return fernet.encrypt(mot_de_passe.encode())

# Décrypter un mot de passe
def decrypt(mot_de_passe_chiffre,key):
	fernet = Fernet(key)
	return fernet.decrypt(mot_de_passe_chiffre.encode()).decode()

def login_test(user,user_password):
	json_create("comptes",{})
	comptes = json_variable("comptes")
	return bool((user in comptes.keys())and (check_password_hash(comptes[user], user_password)))
