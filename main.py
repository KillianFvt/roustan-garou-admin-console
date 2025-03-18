import sys
from db_methods.requests import initialize_game, open_game, start_game, end_game, get_current_game, get_winners, close_game

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def main():
    while True:
        current_game = get_current_game()
        game_state = current_game.state if current_game else None

        print("\n=== Menu Principal ===")
        
        if not current_game or game_state == 3:  # No game or game ended
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
                
                print("\n=== JEU INITIALISE ===")
                print("1. Invitations ouvertes")
                print("2. Retour au menu principal")
                
                init_choice = input("Choisissez une option: ")
                
                if init_choice == "1":
                    open_game()
                    print("La partie est maintenant ouverte aux joueurs.")
                    
                    print("\n=== PARTIE OUVERTE ===")
                    print("1. Commencez la partie (ferme les invitations)")
                    print("2. Retour menu")
                    
                    open_choice = input("Choisissez une option: ")
                    
                    if open_choice == "1":
                        start_game()
                        print("Game a start ! On peut plus join.")
            
            elif choice == "2":
                print("Exit.")
                sys.exit()
                
            else:
                print("Mauvaise réponse, veuillez réessayer.")
                
        elif game_state == 0:  # Game initialized but not open
            print("1. Ouvre les invits")
            print("2. Ferme la partie")
            print("3. Quitter")
            
            choice = input("Choisissez une option: ")
            
            if choice == "1":
                open_game()
                print("La game est ouverte.")
                
            elif choice == "2":
                close_game()
                
            elif choice == "3":
                print("Exit.")
                sys.exit()
                
            else:
                print("Invalide, retry svp.")
                
        elif game_state == 1:  # Game open for invitations
            print("1. Start Game (ferme les invits)")
            print("2. Ferme la partie")
            print("3. Quitter")
            
            choice = input("Choisissez une option: ")
            
            if choice == "1":
                start_game()
                print("La partie est maintenant ouverte aux joueurs.")
                
            elif choice == "2":
                close_game()
                
            elif choice == "3":
                print("Exit.")
                sys.exit()
                
            else:
                print("Invalide, réessayez.")
                
        elif game_state == 2:
            print("1. Obtenir les gagnants")
            print("2. Ferme la partie")
            print("3. Supprime la partie")
            print("4. Quitter")
            
            choice = input("Choisissez une option: ")
            
            if choice == "1":
                get_winners()
                
            elif choice == "2":
                close_game()
                
            elif choice == "3":
                end_game()
                print("Game terminée.")
                
            elif choice == "4":
                print("Exit.")
                sys.exit()
                
            else:
                print("Option invalide, réessayez.")

if __name__ == "__main__":
    main()
