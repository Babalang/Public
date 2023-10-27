import pygame

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre du jeu
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Jeu de Plateforme")

# Chargement de l'image de fond
fond = pygame.image.load("/Users/BastianLangouet/Desktop/perso/projetsperso/autre/fond.png")

# Dimensions de l'image de fond
largeur_fond = fond.get_width()
hauteur_fond = fond.get_height()

# Position de l'arrière-plan
x_fond = 0

# Couleurs
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)

# Variables du joueur
x_joueur = 50
y_joueur = hauteur_fenetre - 100
largeur_joueur = 40
hauteur_joueur = 60
vitesse_joueur = 5

# Boucle principale du jeu
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
    
    # Gestion des commandes du joueur
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        x_joueur -= vitesse_joueur
    if touches[pygame.K_RIGHT]:
        x_joueur += vitesse_joueur

    # Déplacement de l'arrière-plan en fonction de la position du joueur
    x_fond -= vitesse_joueur

    # Affichage de l'arrière-plan
    fenetre.blit(fond, (x_fond, 0))
    fenetre.blit(fond, (x_fond + largeur_fond, 0))

    # Affichage du joueur
    pygame.draw.rect(fenetre, BLEU, (x_joueur, y_joueur, largeur_joueur, hauteur_joueur))

    # Mise à jour de la fenêtre
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()
