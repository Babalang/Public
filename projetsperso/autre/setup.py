from cx_Freeze import setup, Executable
#Création d'un executable (fonctionne moyennement)
setup(name='GestMDP',
      version='1.0',
      description='Gestionnaire de mot de passe',
      executables=[Executable('GestMDPapp.py')])
