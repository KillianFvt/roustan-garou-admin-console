import sys
from db_methods.requests import initialize_game, open_game, start_game

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Démarrer une nouvelle partie")
        print("2. Quitter")
        
        choice = input("Choisissez une option : ")
        
        if choice == "1":
            nb_player = get_int_input("Nombre de joueurs : ")
            map_width = get_int_input("Largeur de la carte : ")
            map_height = get_int_input("Hauteur de la carte : ")
            max_turn_time = get_int_input("Temps max par tour : ")
            max_nb_turn = get_int_input("Nombre maximum de tours : ")
            
            map_size = f"{map_width}x{map_height}"
            game_id = initialize_game(nb_player, map_size, max_nb_turn, max_turn_time)
            
            print(f"Partie créée avec l'ID : {game_id}")
            
            input("Voulez-vous ouvrir la partie pour que les joueurs rejoignent ? (Appuyez sur Entrée pour valider)")
            open_game()
            print("La partie est maintenant ouverte aux joueurs.")
                                
            input("Voulez-vous démarrer la partie ? Empêche que de nouveaux joueurs rejoignent. (Appuyez sur Entrée pour valider)")
            start_game()
            print("La partie est maintenant ouverte aux joueurs.")

        
        elif choice == "2":
            print("Fermeture du programme.")
            sys.exit()
        
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
