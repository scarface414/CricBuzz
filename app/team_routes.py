from fastapi import APIRouter , status , Depends , Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Optional, Union, List, Annotated

from jose import JWTError, jwt

from schemas import MatchModel,TeamModel, SquadModel, Settings, TokenData
from typing import Annotated
from db import engine, Base, Session
from models import Match, Team, squads, Player


router = APIRouter(
    prefix='/api/team',
    tags=['Team API']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")
settings = Settings()

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
)   

db = Session(bind=engine)

@router.get("/")
async def all_teams():
    return db.query(Team).all()


@router.post("/",response_model=TeamModel, status_code=status.HTTP_201_CREATED)
async def create_team(team:TeamModel , token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("subject") 
    except JWTError:
        raise credentials_exception
    
    teamname = db.query(Team).filter(Team.name == team.name).first()
    
    if teamname is not None : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team Exists")
    
    new_team = Team(
        name = team.name
    )

    db.add(new_team)
    db.commit()

    return new_team

@router.get("/{team_id}/squad")
async def get_squad_by_team_id(team_id : int) :
    
    return db.query(Team).filter(Team.team_id == team_id).first().players

@router.post("/{team_id}/squad" , status_code= status.HTTP_201_CREATED)
async def add_player_to_team(player_id : int , team_id : int , token: Annotated[str, Depends(oauth2_scheme)]) :
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("subject") 
    except JWTError:
        raise credentials_exception

    team = db.query(Team).filter(Team.team_id == team_id).first()
    if team is None : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team Does Not Exists")
    
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player Does Not Exists")
    
    player_teams = jsonable_encoder(player.teams)
    player_teams = [current["team_id"] for current in player_teams]

    if team_id in player_teams : 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player Present in Team")

    player.teams.append(team)
    db.commit()

    return {"message" : "Player {} successfully added to Team {}".format(player_id , team_id)}
    



