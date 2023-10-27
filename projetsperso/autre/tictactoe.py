import itertools
import tkinter as tk
#Jeu de tic tac toe.
def display_board(board):
    board_str = ""
    for i in range(3):
        board_str += f"{board[i][0]} | {board[i][1]} | {board[i][2]}" + "\n"
        if i != 2:
            board_str += "--|---|--\n"
    return board_str

def on_button_click(button, position):
    global board, player_marker, game_on, turn_label
    if game_on and button["text"] == "":
        button["text"] = player_marker
        x, y = position
        board[x][y] = player_marker
        if win_check(board, player_marker):
            turn_label["text"] = "Félicitations ! " + turn_label["text"] + " a gagné la partie !"
            game_on = False
        elif full_board_check(board):
            turn_label["text"] = "Match nul !"
            game_on = False
        else:
            player_marker = player1_marker if player_marker == player2_marker else player2_marker
            turn_label["text"] = f"Tour de {turn()}"
            
def turn():
    return "Joueur 1" if player_marker == player1_marker else "Joueur 2"

def new_game():
    global board, player_marker, game_on, turn_label
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    player_marker = player1_marker
    game_on = True
    turn_label["text"] = f"Tour de {turn()}"
    for button in buttons:
        button["text"] = ""


def player_input():
    marker = ''
    while marker not in {'X', 'O'}:
        marker = input("Joueur 1, choisissez X ou O : ").upper()
    return ('X', 'O') if marker == 'X' else ('O', 'X')

def place_marker(board, marker, position):
    board[position[0]][position[1]] = marker

def win_check(board, mark):
    return ((board[0][0] == mark and board[0][1] == mark and board[0][2] == mark) or
    (board[1][0] == mark and board[1][1] == mark and board[1][2] == mark) or
    (board[2][0] == mark and board[2][1] == mark and board[2][2] == mark) or
    (board[0][0] == mark and board[1][0] == mark and board[2][0] == mark) or
    (board[0][1] == mark and board[1][1] == mark and board[2][1] == mark) or
    (board[0][2] == mark and board[1][2] == mark and board[2][2] == mark) or
    (board[0][0] == mark and board[1][1] == mark and board[2][2] == mark) or
    (board[0][2] == mark and board[1][1] == mark and board[2][0] == mark))

import random
def choose_first():
    return 'Joueur 2' if random.randint(0, 1) == 0 else 'Joueur 1'

def space_check(board, position):
    return board[position[0]][position[1]] == ' '

def full_board_check(board):
    return all(
        board[i][j] != ' ' for i, j in itertools.product(range(3), range(3))
    )

def player_choice(board):
    position = ()
    while not position:
        try:
            x, y = map(int, input("Entrez les coordonnées de votre coup (ex. 1 2): ").split())
            if x > 3 or y > 3:
                print("Coordonnées invalides. Veuillez réessayer.")
            elif space_check(board, (x-1, y-1)):
                position = (x-1, y-1)
            else:
                print("Case déjà occupée. Veuillez réessayer.")
        except ValueError:
            print("Coordonnées invalides. Veuillez réessayer.")
    return position

def replay():
    return input("Voulez-vous rejouer ?    ").lower().startswith('o')

print("Bienvenue dans le jeu Tic Tac Toe !")

while True:
# Initialisation du tableau et des variables
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    player1_marker, player2_marker = player_input()
    player_marker = player1_marker
    game_on = True

    # Création de l'interface graphique
    root = tk.Tk()
    root.title("Tic Tac Toe")

    # Affichage du tableau
    board_label = tk.Label(root, text=display_board(board))
    board_label.pack()

    # Affichage du tour
    turn_label = tk.Label(root, text=f"Tour de {turn()}")
    turn_label.pack()

    # Affichage des boutons
    buttons_frame = tk.Frame(root)
    buttons_frame.pack()
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            button = tk.Button(buttons_frame, text="", width=6, height=3, font=("Arial", 30))
            button.grid(row=i, column=j)
            button["command"] = lambda button=button, position=(i, j): on_button_click(button, position)
            row.append(button)
        buttons.append(row)

    # Bouton pour commencer une nouvelle partie
    new_game_button = tk.Button(root, text="Nouvelle partie", command=new_game)
    new_game_button.pack()

    root.mainloop()

    # Détermine qui joue en premier
    turn = choose_first()
    print(f"{turn} commence !")

    # Demande aux joueurs de placer leurs marques
    player1_marker, player2_marker = player_input()

    # Boucle de jeu
    game_on = True
    while game_on:
        if turn == 'Joueur 1':
            # Tour du joueur 1
            display_board(board)
            position = player_choice(board)
            place_marker(board, player1_marker, position)

            # Vérifie si le joueur 1 a gagné
            if win_check(board, player1_marker):
                display_board(board)
                print("Félicitations ! Joueur 1 a gagné la partie !")
                game_on = False
            elif full_board_check(board):
                display_board(board)
                print("Match nul !")
                game_on = False
            else:
                turn = 'Joueur 2'
        else:
            # Tour du joueur 2
            display_board(board)
            position = player_choice(board)
            place_marker(board, player2_marker, position)

            # Vérifie si le joueur 2 a gagné
            if win_check(board, player2_marker):
                display_board(board)
                print("Félicitations ! Joueur 2 a gagné la partie !")
                game_on = False
            elif full_board_check(board):
                display_board(board)
                print("Match nul !")
                game_on = False
            else:
                turn = 'Joueur 1'

    # Propose aux joueurs de rejouer
    if not replay():
        break

