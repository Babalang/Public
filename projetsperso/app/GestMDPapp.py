from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import *
from random import *
from cryptography.fernet import Fernet
from functions import *
from functools import partial

class index(QMainWindow):
    def __init__(self):
        global is_connected
        super().__init__()
        self.setWindowTitle("Accueil")
        self.setGeometry(600, 300, 300, 300) 
        print(is_connected)
        Gen = QPushButton("Générer un mot de passe", self)
        Gen.setGeometry(50, 100, 200, 50)
        Gen.clicked.connect(self.aller_Gen)
        timer = QPushButton("TIMER",self)
        timer.setGeometry(50,160,200,50)
        timer.clicked.connect(self.lance_timer)
        if is_connected == False : 
            bouton = QPushButton("Connexion", self)
            bouton.setGeometry(50, 220, 200, 50)
            bouton.clicked.connect(self.aller_login)
        else: 
            Get = QPushButton("Rechercher un mot de passe", self)
            Get.setGeometry(50, 40, 200, 50)
            Get.clicked.connect(self.aller_Get)     
            deconnexion = QPushButton("Déconnexion", self)
            deconnexion.setGeometry(50, 220, 200, 50)
            deconnexion.clicked.connect(self.deco)
            
    def lance_timer(self):
        self.close()
        os.system(f"python3 {os.getcwd()}/app/Veille.py")
    def aller_login(self):
        self.close()
        self.fenetre2 = login()
        self.fenetre2.show()

    def aller_Gen(self):
        self.close()
        self.Gen = Gen_MDP()
        self.Gen.show()

    def aller_Get(self):
        self.close()
        self.Get = Get_MDP()
        self.Get.show()

    def deco(self):
        global is_connected
        global username
        username = None
        is_connected = False
        self.aller_login()

class login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setGeometry(500, 200, 500, 300)
        titre = QLabel("Connexion / Inscription", self)
        titre.setGeometry(175, 10, 150, 20)
    # Ajouter du texte à la fenetre 2
        texte = QLabel("Entrez votre identifiant :", self)
        texte.setGeometry(50, 60, 150, 20)
        largeur_texte = texte.width()
        self.id_field = QLineEdit(self)
        self.id_field.setGeometry(texte.geometry().x()+ largeur_texte+50, texte.geometry().y()+0, 100, 20)
        texte2 = QLabel("Entrez votre Mot de Passe :", self)
        texte2.setGeometry(50, 110, 200, 20)
        largeur_texte2 = texte2.width()
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setGeometry(texte2.geometry().x()+ largeur_texte2, texte2.geometry().y()+0, 100, 20)
        submit = QPushButton("Connexion",self)
        submit.setGeometry(50,170,200,50)
        submit.clicked.connect(self.Login)
        regist = QPushButton("Inscription",self)
        regist.setGeometry(submit.geometry().x()+submit.width()+10,submit.geometry().y(),200,50)
        regist.clicked.connect(self.Register)
        #Bouton de retour
        bouton = QPushButton("Retour",self)
        bouton.setGeometry(50,230,200,50)
        bouton.clicked.connect(self.aller_Accueil)
        
    def Login(self):
        global is_connected
        global username
        valeur1 = self.id_field.text().lower()
        valeur2 = self.password_field.text()
        if login_test(valeur1,valeur2):
            is_connected = True
            username = valeur1
            self.close()
            self.fenetre1 = index()
            self.fenetre1.show()
        else :
            QMessageBox.warning(self, 'Erreur', 'Identifiant ou mot de passe incorrect')
            self.id_field.clear()
            self.password_field.clear()
    
    def Register(self):  # sourcery skip: extract-method
        global is_connected
        global username
        if is_connected == False :
            user_id = self.id_field.text().lower()
            user_password = self.password_field.text().lower()
            comptes = json_variable("comptes")
            if (user_id not in comptes.keys()):
                json_create(f"{user_id}_chiffrement",{})
                json_create(f"{user_id}_MotDePasse",{})
                comptes[user_id] = generate_password_hash(user_password)
                json_sendVariable("comptes", comptes)
                is_connected = True
                username = user_id
                self.aller_Accueil()
                
    def aller_Accueil(self):
        self.close()
        self.fenetre1 = index()
        self.fenetre1.show()

class Gen_MDP(QMainWindow):
    def __init__(self):
        global is_connected
        global username
        super().__init__()
        self.setWindowTitle("Genérer un mot de passe")
        self.setGeometry(500, 200, 800, 300)
        global Mot
        Mot = createMDP()
        texteMDP = QLabel(f"Voici un mot de passe : {Mot}", self)
        texteMDP.setGeometry(10, 60, 580, 20)
        copy = QPushButton("Copier",self)
        copy.setGeometry(texteMDP.geometry().x()+550,texteMDP.geometry().y(),150,20)
        copy.clicked.connect(self.copier)
        #Bouton de retour
        bouton = QPushButton("Retour",self)
        bouton.setGeometry(50,230,200,50)
        bouton.clicked.connect(self.aller_Accueil)
        if is_connected == True:
            texte = QLabel("Entrez un libellé :", self)
            texte.setGeometry(50, 110, 150, 20)
            largeur_texte = texte.width()
            self.id_field = QLineEdit(self)
            self.id_field.setGeometry(texte.geometry().x()+ largeur_texte+50, texte.geometry().y()+0, 100, 20)
            submit = QPushButton("Enregistrer",self)
            submit.setGeometry(50,170,200,50)
            submit.clicked.connect(self.enregistrer)
    
    def enregistrer(self):  # sourcery skip: extract-method
        global is_connected
        global username
        global Mot
        if is_connected:
            valeur1 = self.id_field.text().lower()
            valeur2 = Mot
            chiffrement = json_variable(f"{username}_chiffrement")
            MotDePasse = json_variable(f"{username}_MotDePasse")
            key = Fernet.generate_key()
            MotDePasse[valeur1] = encrypt(valeur2,key).decode("UTF-8")
            chiffrement[valeur1] = key.decode("UTF-8")
            json_sendVariable(f"{username}_MotDePasse",MotDePasse)
            json_sendVariable(f"{username}_chiffrement",chiffrement)
            key = None
            Mot = None
        self.aller_Accueil()

    def copier(self):
        global Mot
        clipboard = QApplication.clipboard()
        clipboard.setText(Mot)
        QMessageBox.information(self, "Copier", "Texte copié dans le presse-papiers !")

    def aller_Accueil(self):
        self.close()
        self.fenetre1 = index()
        self.fenetre1.show()

class Get_MDP(QMainWindow):
    def __init__(self):
        super().__init__()
        global is_connected
        global username
        self.setWindowTitle("Trouver un mot de passe")
        self.setGeometry(500, 200, 500, 300)
        #Bouton de retour
        bouton = QPushButton("Retour",self)
        bouton.setGeometry(150,230,200,50)
        bouton.clicked.connect(self.aller_Accueil)
        donnees = json_variable(f"{username}_MotDePasse")
        self.table = QTableWidget(len(donnees), 3, self)
        for index,elem in enumerate(donnees.keys()):
            self.table.setItem(index, 0, QTableWidgetItem(elem))
            copy_button = QPushButton("Copier")
            copy_button.clicked.connect(partial(self.rechercher, elem))
            self.table.setCellWidget(index, 1, copy_button)
            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(partial(self.supprimer, elem))
            self.table.setCellWidget(index, 2, delete_button)
        self.table.setHorizontalHeaderLabels(["Libellés"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setGeometry(0,0,500,200)
    def aller_Accueil(self):
        self.close()
        self.fenetre1 = index()
        self.fenetre1.show()
    
    def rechercher(self,valeur2):  # sourcery skip: extract-method
        global is_connected
        global username
        if is_connected:
            alert = QMessageBox()
            if (valeur2 in json_variable(f"{username}_MotDePasse").keys()):
                chiffrement = json_variable(f"{username}_chiffrement")[valeur2]
                MotDePass = json_variable(f"{username}_MotDePasse")[valeur2]
                clipboard = QApplication.clipboard()
                clipboard.setText(f"{decrypt(MotDePass,chiffrement)}")
                alert.setText("Mot de passe copié")
            else : 
                alert.setText("Libellé inexistant")
        else : 
            self.aller_Accueil()

    def supprimer(self,libelle):  # sourcery skip: extract-method
        global is_connected
        global username
        if is_connected:
            alert = QMessageBox()
            if libelle in json_variable(f"{username}_MotDePasse").keys():
                chiffrement = json_variable(f"{username}_chiffrement")
                MotDePass = json_variable(f"{username}_MotDePasse")
                chiffrement.pop(libelle)
                MotDePass.pop(libelle)
                json_sendVariable(f"{username}_MotDePasse",MotDePass)
                json_sendVariable(f"{username}_chiffrement",chiffrement)
                rows_to_delete = []
                for row in range(self.table.rowCount()):
                    item = self.table.item(row, 0)  # On suppose que la valeur à comparer est dans la colonne 0
                    if item and item.text() == libelle:
                        rows_to_delete.append(row)
                for row in rows_to_delete:
                    self.table.removeRow(row)
                alert.setText("Mot de passe supprimé")
            else : 
                alert.setText("Libellé inexistant")
        else : 
            self.aller_Accueil()
    
# Créer l'application et afficher la fenetre 1
global is_connected
global username
username = None
is_connected = False
app = QApplication([])
css_file = QFile(f"{os.getcwd()}/app/static/style.css")
css_file.open(QFile.ReadOnly)
app.setStyleSheet(css_file.readAll().data().decode("utf-8"))
css_file.close()
app.setWindowIcon(QIcon(f"{os.getcwd()}/app/static/Gest.jpeg"))
fenetre1 = index()
fenetre1.show()
app.exec()