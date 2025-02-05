from sqlalchemy.orm import sessionmaker
from models import Game, Player, GamePlayer, engine

SessionLocal = sessionmaker(bind=engine)

# une game en cours d'initialisation a un état de 0
def initialize_game(nb_player, map_size, max_nb_turn, max_turn_time):
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

# démarrer la game revient à mettre son état à 1
def start_game(game_id):
    session = SessionLocal()
    game = session.query(Game).filter(Game.id == game_id).first()
    if game:
        game.state = 1
        session.commit()
    session.close()

# après la win (game terminée => state = 2)
def end_game(game_id):
    session = SessionLocal()
    game = session.query(Game).filter(Game.id == game_id).first()
    if game:
        game.state = 2
        session.commit()
    session.close()


# quand le joueur créé le compte
def add_player(player_name):
    session = SessionLocal()
    new_player = Player(name=player_name)
    session.add(new_player)
    session.commit()
    session.refresh(new_player)
    session.close()
    return new_player.id

# quand un joueur se connecte
def connect_player(game_id, player_id, is_wolf):
    session = SessionLocal()
    game_player = GamePlayer(id_game=game_id, id_player=player_id, is_wolf=is_wolf)
    session.add(game_player)
    session.commit()
    session.close()