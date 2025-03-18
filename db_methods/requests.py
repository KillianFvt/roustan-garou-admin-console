from sqlalchemy.orm import sessionmaker
from db_methods.models import Game, Player, GamePlayer, engine

SessionLocal = sessionmaker(bind=engine)

def get_current_game():
    session = SessionLocal()
    game = session.query(Game).order_by(Game.id.desc()).first()
    session.close()
    return game

# a game that is being initialized has a state of 0
def initialize_game(nb_player: int, map_size: str, max_nb_turn: int, max_turn_time: int) -> int:
    session = SessionLocal()
    new_game = Game(
        nb_player=nb_player,
        map_size=map_size,
        max_nb_turn=max_nb_turn,
        max_turn_time=max_turn_time,
        state=0
    )
    session.add(new_game)
    session.commit()
    session.refresh(new_game)
    session.close()
    return new_game.id


# open the game (game open => state = 1)
def open_game():
    session = SessionLocal()
    game = session.query(Game).order_by(Game.id.desc()).first()
    if game:
        game.state = 1
        session.commit()
    session.close()

# start the game (game started => state = 2)
def start_game():
    session = SessionLocal()

    game = session.query(Game).order_by(Game.id.desc()).first()
    if game:
        game.state = 2
        session.commit()
    session.close()

# after the game is over (game ended => state = 3)
def end_game():
    session = SessionLocal()

    game = session.query(Game).order_by(Game.id.desc()).first()
    if game:
        game.state = 3
        session.commit()
    session.close()

# Gets winners (juste les gens en vie)
def get_winners():
    session = SessionLocal()
    game = session.query(Game).order_by(Game.id.desc()).first()
    
    if not game or game.state < 2:
        print("Aucune game en cours.")
        session.close()
        return
    
    game_players = session.query(GamePlayer).filter(GamePlayer.id_game == game.id, GamePlayer.is_alive == True).all()
    
    if not game_players:
        print("Aucun gagnant trouvé.")
    else:
        print("\n=== GAGNANTS ===")
        for gp in game_players:
            player = session.query(Player).filter(Player.id == gp.id_player).first()
            role = "Wolf" if gp.is_wolf else "Villager"
            print(f"- {player.name} ({role})")
    
    session.close()

def close_game():
    session = SessionLocal()
    game = session.query(Game).order_by(Game.id.desc()).first()
    
    if not game:
        print("Aucune game trouvée.")
        session.close()
        return
    
    session.query(GamePlayer).filter(GamePlayer.id_game == game.id).delete()
    session.query(Game).filter(Game.id == game.id).delete()
    
    session.commit()
    session.close()
    print("Game fermée et supprimée de la db.")

# to add a player to the db
def add_player(player_name: str) -> int:
    session = SessionLocal()
    new_player = Player(name=player_name)
    session.add(new_player)
    session.commit()
    session.refresh(new_player)
    session.close()
    return new_player.id

# when a player connects to a game
def connect_player(player_name: str) -> None:
    session = SessionLocal()

    # if player is not in db then add him
    player = session.query(Player).filter(Player.name == player_name).first()
    if not player:
        player_id = add_player(player_name)
    else :
        player_id = player.id

    # get the last game id
    game_id = session.query(Game).order_by(Game.id.desc()).first().id

    game_player = GamePlayer(id_game=game_id, id_player=player_id, is_wolf=False)
    session.add(game_player)
    session.commit()
    session.close()