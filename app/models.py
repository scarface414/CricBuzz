from db import Base
from sqlalchemy import Column, Integer, String, DateTime , Text , Boolean , ForeignKey, Date, Table
import datetime
from sqlalchemy.orm import relationship

class User(Base) : 
    __tablename__ = 'users'

    user_id = Column(Integer , primary_key=True)
    username = Column(String(25) , unique = True , nullable=False) 
    email = Column(String(100) , unique=True , nullable=False)
    password = Column(Text , nullable = True)
    is_admin = Column(Boolean , default = False)


class Player(Base) :
    __tablename__ = 'players'

    player_id = Column(Integer , primary_key=True)
    name = Column(String(25) ,  nullable=False) 
    matches_played = Column(Integer)
    runs = Column(Integer)
    wickets = Column(Integer)

    teams = relationship("Team", secondary="squads", back_populates='players')
    

class Match(Base):
    __tablename__ = "matches"
    match_id = Column(Integer, primary_key=True)
    venue = Column(String)
    datetime = Column(DateTime)

    team1_id = Column(Integer, ForeignKey("teams.team_id"))
    team2_id = Column(Integer, ForeignKey("teams.team_id"))

    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])


class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True)
    name = Column(String)

    matches = relationship(
        "Match",
        primaryjoin="or_(Match.team2_id == Team.team_id , Match.team1_id == Team.team_id)",
    )
    players = relationship("Player", secondary="squads", back_populates='teams')

squads = Table('squads', Base.metadata,
    Column('team_id', ForeignKey('teams.team_id'), primary_key=True),
    Column('player_id', ForeignKey('players.player_id'), primary_key=True)
)
