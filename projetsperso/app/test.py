from pynput import mouse, keyboard
import time

# Temps d'inactivité en secondes avant d'exécuter l'action
global temps_inactivite 
temps_inactivite = 5

# Variable pour stocker le dernier moment où une action a été détectée
global derniere_action 
derniere_action = time.time()

# Variable pour indiquer si le délai d'inactivité a expiré
delai_expire = False

def on_action_detectee():
    print("Action exécutée !")

def on_move(x, y):
    mettre_a_jour_derniere_action()

def on_click(x, y, button, pressed):
    mettre_a_jour_derniere_action()

def on_scroll(x, y, dx, dy):
    mettre_a_jour_derniere_action()

def on_press(key):
    mettre_a_jour_derniere_action()

def mettre_a_jour_derniere_action():
    global derniere_action
    derniere_action = time.time()
    # Réinitialise la variable delai_expire à False
    global delai_expire
    delai_expire = False

def fun():
    global delai_expire
    global temps_inactivite
    # Crée une instance de l'écouteur de souris
    listener_souris = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)

    # Crée une instance de l'écouteur de clavier
    listener_clavier = keyboard.Listener(
        on_press=on_press)

    # Démarre les écouteurs
    listener_souris.start()
    listener_clavier.start()

    # Boucle principale
    while True:
        # Vérifie si le temps écoulé dépasse le seuil d'inactivité
        if not delai_expire and time.time() - derniere_action > temps_inactivite:
            delai_expire = True

        # Exécute l'action lorsque le délai expire
        if delai_expire:
            on_action_detectee()
            return 0

        # Attends un peu avant de vérifier à nouveau
        time.sleep(1)

fun()   