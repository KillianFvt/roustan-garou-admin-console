from sqlalchemy.orm import sessionmaker

from db_methods.db_exceptions import MaxPlayersReachedException
from db_methods.models import Game, Player, GamePlayer, engine

SessionLocal = sessionmaker(bind=engine)

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


# start the game (game started => state = 1)
def start_game(game_id):
    session = SessionLocal()
    game = session.query(Game).filter(Game.id == game_id).first()
    if game:
        game.state = 1
        session.commit()
    session.close()

# after the game is over (game ended => state = 2)
def end_game():
    session = SessionLocal()

    game = session.query(Game).order_by(Game.id.desc()).first()
    if game:
        game.state = 2
        session.commit()
    session.close()

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
    else:
        player_id = player.id

    # get the last game
    game = session.query(Game).order_by(Game.id.desc()).first()

    # check if the game has reached the maximum number of players
    current_player_amt = session.query(GamePlayer).filter(GamePlayer.id_game == game.id).count()
    if current_player_amt >= game.nb_player:
        session.close()
        raise MaxPlayersReachedException()

    game_player = GamePlayer(id_game=game.id, id_player=player_id, is_wolf=False)
    session.add(game_player)
    session.commit()
    session.close()