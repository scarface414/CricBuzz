from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class dbSettings(BaseModel) : 
    user : str = 'postgres' #your username
    password : str = 'abcd' #your password
    host : str = 'localhost'
    port : str = '5432'
    database : str = 'cricbuzzprod' #your database name

class MatchModel(BaseModel) : 
    match_id : Optional[int]  = 0
    venue : str
    datetime : datetime

    team1_id : int 
    team2_id : int 

class TeamModel(BaseModel) : 
    team_id : Optional[int] = 0
    name : str

class UserModel(BaseModel) : 
    user_id : Optional[int] = 0
    username : str
    email : str
    password : str

class AdminModel(UserModel) : 
    is_admin : bool = True

class Settings(BaseModel) :
    SECRET_KEY : str = 'dd9ab4518374d959e38304faf35303c980246be9c6dec0fb17fa694f51d44d5c' 
    ALGORITHM : str =  "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30

class PlayerModel(BaseModel) : 
    player_id : Optional[int] = 0
    name : str
    matches_played : int
    runs : int
    wickets : int

class SquadModel(BaseModel) : 
    player_id : int
    team_id : int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel) : 
    username : str
