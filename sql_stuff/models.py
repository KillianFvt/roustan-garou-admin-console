from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base

DATABASE_URL = "sqlite:///database.db"  

Base = declarative_base()

class Game(Base):
    __tablename__ = "Game"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nb_player = Column(Integer, nullable=False)
    map_size = Column(String, nullable=False)
    max_nb_turn = Column(Integer, nullable=False)
    max_turn_time = Column(Integer, nullable=False)
    turn_number = Column(Integer, default=0)
    state = Column(Integer, default=0, nullable=False)

    players = relationship("GamePlayer", back_populates="game")

class Player(Base):
    __tablename__ = "Player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    games = relationship("GamePlayer", back_populates="player")

class GamePlayer(Base):
    __tablename__ = "Game_player"

    id_game = Column(Integer, ForeignKey("Game.id"), primary_key=True)
    id_player = Column(Integer, ForeignKey("Player.id"), primary_key=True)
    is_alive = Column(Boolean, default=True, nullable=False)
    is_wolf = Column(Boolean, default=False, nullable=False)

    game = relationship("Game", back_populates="players")
    player = relationship("Player", back_populates="games")

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)