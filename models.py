from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

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

    players = relationship("GamePlayer", back_populates="Game")

class Player(Base):
    __tablename__ = "Player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    Games = relationship("GamePlayer", back_populates="Player")

class GamePlayer(Base):
    __tablename__ = "Game_player"

    id_game = Column(Integer, ForeignKey("Game.id"), primary_key=True)
    id_player = Column(Integer, ForeignKey("Player.id"), primary_key=True)
    is_alive = Column(Boolean, default=True, nullable=False)
    role = Column(Boolean, nullable=False)

    Game = relationship("Game", back_populates="players")
    player = relationship("Player", back_populates="Games")
